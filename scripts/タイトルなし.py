from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.conf import settings
import os
import csv
import pandas as pd
import re
import spacy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from .forms import WordListForm

# ストップワードをCSVから読み込む
def load_stopwords_from_csv(stopwords_csv):
    stopwords = []
    try:
        with open(stopwords_csv, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    stopwords.append(row[0])  # CSVの1列目にストップワードが格納されていると仮定
        return stopwords
    except Exception as e:
        print(f"ストップワードの読み込みエラー: {e}")
        return []

# SpaCyモデル設定
def setup_spacy_model():
    try:
        nlp = spacy.load("ja_core_news_lg")
        return nlp
    except Exception as e:
        print(f"SpaCyモデル読み込みエラー: {e}")
        return None

# テキスト解析
def analyze_texts(nlp, texts, stopwords):
    results = []
    for text in texts:
        if not text.strip():
            continue
        doc = nlp(text)
        for token in doc:
            if token.text not in stopwords and token.is_alpha and token.pos_ != "ADP":
                results.append([token.text, token.lemma_, token.pos_])
    return results

# 日本語チェック
def is_japanese(text):
    pattern = re.compile(r'[ぁ-んァ-ン一-龯]')
    return bool(pattern.search(text))

# 日本語テキストのみにフィルタリング
def filter_japanese_texts(texts):
    return [text for text in texts if is_japanese(text)]

# 日本語以外の行を削除
def remove_non_japanese_rows(df):
    df = df[df['テキスト'].apply(is_japanese)]
    return df

# Google Sheetsにアップロード
def upload_to_google_sheets(sheet_id, sheet_name, df):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "C:\\Users\\81908\\Downloads\\aerial-antonym-444302-f9-9ff7a2c99cca.json"
        )
        client = gspread.authorize(credentials)
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.clear()

        worksheet.append_row(list(df.columns))  # ヘッダー
        for row in df.values:
            worksheet.append_row(row.tolist())  # データ行
    except Exception as e:
        print(f"Google Sheetsアップロードエラー: {e}")

# テキストファイルの処理
def process_text(file_path, words_to_count, output_file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    word_counts = {word: 0 for word in words_to_count}

    for word in words_to_count:
        word_counts[word] = text.count(word)
        text = text.replace(word, '')

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("ワード出現回数:\n")
        for word, count in word_counts.items():
            output_file.write(f"{word}: {count}\n")

# ビュー関数
def home(request):
    context = {}

    if request.method == 'POST':
        form = WordListForm(request.POST)
        if form.is_valid():
            words_input = form.cleaned_data['words']
            words_to_count = [word.strip() for word in words_input.split(',')]

            if request.FILES.get('file'):
                uploaded_file = request.FILES['file']
                fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                filename = fs.save(uploaded_file.name, uploaded_file)
                file_path = fs.url(filename)

                uploaded_file_path = fs.path(filename)
                base_filename, file_extension = os.path.splitext(filename)
                output_filename = base_filename + '_結果.txt'
                output_file_path = os.path.join(settings.MEDIA_ROOT, output_filename)

                try:
                    process_text(uploaded_file_path, words_to_count, output_file_path)

                    # ストップワードとテキスト処理
                    stopwords_csv = "D:\\python\\stopwords.csv"
                    stopwords = load_stopwords_from_csv(stopwords_csv)
                    nlp = setup_spacy_model()
                    if not nlp:
                        context = {'error': "SpaCyモデルの読み込みに失敗しました", 'form': form}
                    else:
                        with open(uploaded_file_path, 'r', encoding='utf-8') as f:
                            texts = f.readlines()
                        japanese_texts = filter_japanese_texts(texts)
                        analyzed_data = analyze_texts(nlp, japanese_texts, stopwords)
                        df = pd.DataFrame(analyzed_data, columns=["テキスト", "原型", "品詞"])

                        df = remove_non_japanese_rows(df)
                        text_counts = df['テキスト'].value_counts()
                        df['出現回数'] = df['テキスト'].map(text_counts)

                        google_sheet_id = "your_google_sheet_id"
                        google_sheet_name = "your_sheet_name"
                        upload_to_google_sheets(google_sheet_id, google_sheet_name, df)

                    context = {
                        'file_path': file_path,
                        'filename': filename,
                        'output_file_path': fs.url(output_filename),
                        'form': form
                    }

                except Exception as e:
                    context = {'error': f"処理中にエラーが発生しました: {str(e)}", 'form': form}
            else:
                context = {'error': "ファイルがアップロードされていません。", 'form': form}
        else:
            context = {'error': "入力された単語リストに問題があります。", 'form': form}
    else:
        form = WordListForm()

    context['form'] = form
    return render(request, 'home.html', context)
