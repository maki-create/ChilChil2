import pandas as pd
import re
from transformers import pipeline
from fugashi import Tagger  # 日本語形態素解析

# 1. 辞書ファイルの読み込み
dictionary_file = "sentiment_words.csv"  # 辞書ファイルのパス
dictionary_data = pd.read_csv(dictionary_file)

# 辞書のポジティブ・ネガティブ単語セットを作成
positive_words = set(dictionary_data[dictionary_data['sentiment'] == 'positive']['word'])
negative_words = set(dictionary_data[dictionary_data['sentiment'] == 'negative']['word'])

# 2. ストップワードファイルの読み込み
stop_words_file = "stopwords.csv"  # ストップワードファイルのパス
stop_words_data = pd.read_csv(stop_words_file, header=None)  # ヘッダーがない場合
stop_words = set(stop_words_data[0])  # 1列目にストップワードが格納されていると仮定

# 3. データの読み込み
file_path = "tweets.xlsx"  # CSVの場合は "tweets.csv"
sheet_name = "Sheet1"

# ExcelまたはCSVデータを読み込み
if file_path.endswith(".xlsx"):
    data = pd.read_excel(file_path, sheet_name=sheet_name)
elif file_path.endswith(".csv"):
    data = pd.read_csv(file_path)
else:
    raise ValueError("Supported file formats are .xlsx and .csv only.")

# ツイートの列名を指定
tweet_column = "tweets"
if tweet_column not in data.columns:
    raise ValueError(f"Column '{tweet_column}' not found in the dataset.")

# 4. Sentiment Analysisパイプラインのセットアップ（BERTなど）
classifier = pipeline("sentiment-analysis")

# 5. 日本語形態素解析用のTaggerをセットアップ
tagger = Tagger()

# 6. ツイートからURLや特殊文字を削除する関数
def clean_tweet(tweet):
    # URLや特殊文字を正規表現で削除
    tweet = re.sub(r'http[s]?://\S+', '', tweet)  # URLを削除
    tweet = re.sub(r'[@#]\S+', '', tweet)  # @や#を含む部分を削除
    tweet = re.sub(r'[^A-Za-z0-9一-龯ぁ-んァ-ンー々〆〤]+', ' ', tweet)  # 日本語以外の文字を削除
    return tweet.strip()

# 7. ネガポジ判定ロジック（辞書とBERTモデルの併用）
def analyze_sentiment(tweet):
    # ツイートを事前にクリーンアップ
    tweet = clean_tweet(tweet)

    # ログの初期化
    log = f"Processing Tweet: {tweet}\n"

    # 1. ツイートを単語分割
    words = [word.surface for word in tagger(tweet)]  # 形態素解析で単語に分割
    filtered_words = [word for word in words if word not in stop_words]  # ストップワードを除外

    log += f"Filtered Words: {filtered_words}\n"

    # 2. 分割した単語に対して辞書ベースのネガポジ判定
    positive_score = 0
    negative_score = 0

    for word in filtered_words:
        if word in positive_words:
            positive_score += 1  # ポジティブ単語スコア加算
        elif word in negative_words:
            negative_score += 1  # ネガティブ単語スコア加算

    log += f"Positive Score (Dictionary): {positive_score}, Negative Score (Dictionary): {negative_score}\n"

    # 3. 分割した単語に対してBERTモデルによるネガポジ判定
    model_positive_score = 0
    model_negative_score = 0

    for word in filtered_words:
        try:
            # BERTモデルで各単語に対して判定
            result = classifier(word[:512])  # 長い単語は512文字にトリム
            model_result = result[0]['label']
            if model_result == "POSITIVE":
                model_positive_score += 1
            elif model_result == "NEGATIVE":
                model_negative_score += 1

            log += f"Word: {word}, Model Result: {model_result}\n"
        except Exception as e:
            log += f"Error for word '{word}': {e}\n"

    log += f"Positive Score (Model): {model_positive_score}, Negative Score (Model): {model_negative_score}\n"

    # 4. 辞書とモデルのスコアを統合
    total_positive_score = positive_score + model_positive_score
    total_negative_score = negative_score + model_negative_score

    # 5. スコアを比較して最終判定
    if total_positive_score > total_negative_score:
        final_result = "POSITIVE"
    elif total_negative_score > total_positive_score:
        final_result = "NEGATIVE"
    else:
        final_result = "NEUTRAL"

    log += f"Final Result: {final_result}\n"
    print(log)  # ログ出力
    return final_result

# 各ツイートに対してネガポジ判定を実行
data['Sentiment'] = data[tweet_column].apply(analyze_sentiment)

# 8. 結果の保存
output_file = "tweets_with_sentiment.xlsx"  # CSVの場合は "tweets_with_sentiment.csv"
if output_file.endswith(".xlsx"):
    data.to_excel(output_file, index=False)
elif output_file.endswith(".csv"):
    data.to_csv(output_file, index=False)
else:
    raise ValueError("Supported output file formats are .xlsx and .csv only.")

print(f"Sentiment analysis results saved to {output_file}")
