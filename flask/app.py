from flask import Flask, request, jsonify
import tweepy

app = Flask(__name__)

# APIキーとトークン
bearer_token = "AAAAAAAAAAAAAAAAAAAAANTnwwEAAAAA7u5pfQAwgdk9zR6mwue8MNzasZM%3DHOWML6ApguiVE3Hr35eY7X61tW74gq05jduaWgems1HWax7kRt"   # ここに自身のBearer Tokenを設定

# Tweepyクライアントの作成
client = tweepy.Client(bearer_token)

@app.route('/get_tweets', methods=['POST'])
def query_get():
    # ユーザーからの入力を取得
    query = request.form.get('query')  # 検索クエリ
    start_time = request.form.get('start_time')  # 開始日時
    end_time = request.form.get('end_time')  # 終了日時

    if not query or not start_time or not end_time:
        return jsonify({"error": "クエリ、開始日時、終了日時はすべて必須です"}), 400

    total_count = 0  # ツイート総数
    next_token = None  # ページネーション用トークン

    try:
        while True:
            # APIリクエスト
            response = client.search_recent_tweets(
                query=query,
                start_time=start_time,
                end_time=end_time,
                max_results=100,  # 一度に取得できる最大件数
                next_token=next_token  # ページネーション用トークン
            )

            if response.data:
                total_count += len(response.data)  # ツイート件数を加算

            # 次のページがあるか確認
            if "next_token" in response.meta:
                next_token = response.meta["next_token"]
            else:
                break  # 次のページがなければ終了

        return jsonify({"total_tweets": total_count}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
