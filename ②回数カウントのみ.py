import csv
import pandas as pd
import re
from transformers import pipeline
import spacy

# --- ストップワードのCSV読み込み ---
def load_stopwords_from_csv(stopwords_csv):
    stopwords = []
    try:
        with open(stopwords_csv, mode='r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                if row:  # 空行をスキップ
                    stopwords.append(row[0])  # CSVの1列目にストップワードが格納されていると仮定
        print(f"ストップワードを読み込みました: {len(stopwords)}語")
        return stopwords
    except Exception as e:
        print(f"ストップワードの読み込みエラー: {e}")
        return []

# --- SpaCy モデル設定 ---
def setup_spacy_model():
    try:
        nlp = spacy.load("ja_core_news_lg")
        print("SpaCyモデル読み込み成功")
        return nlp
    except Exception as e:
        print(f"SpaCyモデル読み込みエラー: {e}")
        return None

# --- テキスト解析 ---
def analyze_texts(nlp, texts, stopwords):
    results = []
    for text in texts:
        if not text.strip():
            continue
        doc = nlp(text)
        for token in doc:
            # ストップワードおよび不要なトークン（品詞がADPや不要なもの）を除外
            if token.text not in stopwords and token.is_alpha and token.pos_ != "ADP":
                results.append([token.text, token.lemma_, token.pos_])  # リストとして保存
    return results

# 日本語の正規表現を定義
def is_japanese(text):
    # 日本語（ひらがな、カタカナ、漢字）の文字が含まれているかを確認する正規表現
    pattern = re.compile(r'[ぁ-んァ-ン一-龯]')
    return bool(pattern.search(text))

# A列の日本語正規表現にマッチしない行を削除する処理
def remove_non_japanese_rows(df):
    # A列のテキストが日本語にマッチしない行を削除
    df = df[df['原型'].apply(is_japanese)]
    # 削除後のデータをログ出力
    print("日本語正規表現にマッチしたデータのみ残っています:")
    print(df.head())
    return df

# --- センチメント分析初期化 ---
sentiment_analyzer = pipeline("sentiment-analysis")

def sentiment_analysis(text, row_index):
    try:
        result = sentiment_analyzer(text)
        label = result[0]['label']
        print(f"[行 {row_index}] センチメント分析: テキスト='{text}' => 結果='{label}'")  # 行番号を含めたログ出力
        return 1 if label == "POSITIVE" else -1 if label == "NEGATIVE" else 0
    except Exception as e:
        print(f"[行 {row_index}] センチメント分析エラー: テキスト='{text}', エラー: {e}")
        return 0

# --- テキストファイルからデータを読み込む関数 ---
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            texts = file.readlines()
        # 改行文字を取り除く
        texts = [text.strip() for text in texts if text.strip()]  # 空行を除外
        print(f"テキストファイルから {len(texts)} 行のデータを読み込みました")
        return texts
    except Exception as e:
        print(f"テキストファイル読み込みエラー: {e}")
        return []

# 日本語テキストのみを抽出する関数
def filter_japanese_texts(texts):
    return [text for text in texts if is_japanese(text)]


# --- メイン処理 ---
def main():
    input_text_file = "D:\\python\\先生\\ふったらどしゃぶり　1話.txt"  # テキストファイルのパス
    output_file_excel = "D:\\python\\output.xlsx"  # エクセルファイルのパス
    stopwords_csv = "D:\\python\\stopwords.csv"  # ストップワードCSVのパス

    # テキストファイルのデータを読み込む
    texts = read_text_file(input_text_file)
    if not texts:
        return

    # ストップワードをCSVから読み込み
    stopwords = load_stopwords_from_csv(stopwords_csv)

    # SpaCy モデルのセットアップ
    nlp = setup_spacy_model()
    if not nlp:
        return

    # 日本語テキストのみにフィルタリング
    japanese_texts = filter_japanese_texts(texts)

    # テキスト解析
    analyzed_data = analyze_texts(nlp, japanese_texts, stopwords)

    # DataFrameを作成（3列: テキスト, 原型, 品詞）
    df = pd.DataFrame(analyzed_data, columns=["テキスト", "原型", "品詞"])

    # 日本語正規表現以外を行ごと削除
    df = remove_non_japanese_rows(df)

    # 出現回数をカウント
    text_counts = df['テキスト'].value_counts()  # 'テキスト'ごとの出現回数を計算
    df['出現回数'] = df['テキスト'].map(text_counts)  # 出現回数を元のDataFrameにマッピング

 
    # エクセルファイルに保存
    try:
        df.to_excel(output_file_excel, index=False)
        print(f"エクセルファイルに保存しました: {output_file_excel}")
    except Exception as e:
        print(f"エクセル保存エラー: {e}")

if __name__ == "__main__":
    main()
