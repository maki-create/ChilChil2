import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Streamlit Secretsから情報を取得
google_credentials = st.secrets["google_credentials"]

# TOMLの設定情報を辞書として利用
creds_dict = {
     "type": "service_account",
  "project_id": "aerial-antonym-444302-f9",
  "private_key_id": "e2c40c313a5d840a2cfe97fe2d65c33abd2f975d",
  "private_key": """-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCorQ4EWMLSLWID\nXUtFGr6QdEErmr1Hk8P189Ym9i9O0lXjaxMnzbnIbsJHi7Ds+CM6zR4giu1yHrl0\n1a0ceyx6duL/I5NbFXoWSgTVbsS9Kx3wx1losT29EBvSsK+GQ7qIHn7AQBD4Ldyx\n17rAWUr9qpCh3WcU2RKQTTRvAZQcHuSo0gGB0bgGJnQlIITT60ffstK4QYXdj+5Y\nTX1pN9f7f8ZzguDjElWkbA+hS6M/rjCnnkX27hNEQG/4wv1NO9eNnCNHfnkotVm1\nWWaFT9Mzg29W744B+jjAFnpyu+mAntvZzmCyGvWu5vIq6iqAk9dI9AZd/p1ZvOOv\nvSB+6fO5AgMBAAECggEAEvWkwjNR7rsALd2iNMnNSsJugt65UN7Yo4A9fZKlfagh\n1Fa4R/yVWeStPMqEYBaCKz1cGg9TokS21t2fwDhOJxPO7xvKF+5hkzjNs0nonlTG\n4EYgFCb8CBDT98o5aI+bW2qGF8j7v1G0YV8c1DsVNU8jQ7Z1vD+sGQE8mA+m3MQj\nSS/ZWGS8XZ32lb+/GA34Jp7FVXRzSvMRW1AnILKRVVzr9fAZFegWCyWsJt+dtm1c\nHpIVBjZGfUwqlNFJKnxPoPoi5QKLrkAQBDJteq8m3/wnCH93ssXjFHfOTLadJO9J\nMaAs5ycUQRVfCZx3KQbyHh04/1g5lMPp2s4imlViQQKBgQDjw/eGA/wKXx6/Vah2\nlEM6aWokRE8p+UmKBhqhKfToXC/nVlIYJs7U0dh4t48OkDySzqr97wJ4TPxiq4VO\nD2yyIaXk0Luqa66S3uiz2VtInPBAof0WZoiG4I+3YpU8sjehvlBOia3AJUpGG8U4\np20uW8aZpCZfJegSMtLo7MfZkQKBgQC9lejnP7IH/sRraDEvQKUKFocY9a7hJsKe\njVQnnKIRfY8b2Q6xEbZyaOfjI8fJCZ9dqcANwlYqQ0wwKJCe3SXC6EuHmB/4iN9t\no0mPp77mVBfzlq2d6a9ic+Llujre7yjKavUPfO0vsY4SdM+aGZPPhDKL9zEE8vMe\nKROF3jSjqQKBgCL2VeyQeAPvjfy43V82awtwWwauJai/x3YUccoDcsCoRgIw0fE7\nI8yvWZdONft6UJIIf17zbWGiD6vlwFS3MWw2lgyFrgj+9pE8/mN9HfILhSWmt/7U\nRmjN18HCtD3Y7Yk6eYFUyQMRtlEEukV0DeJr3BSBihJY80K34oA2uIbBAoGAKJm5\nFgTzCHlL8UCP//GVJpLqfbLnr7oQRco4cn89ygccpbcXSV5ktx22Q1N/TpNr+LAI\nvCmZMFXXNB0L06nCk3oR6sjuV9hgGOe2MjiXTlZGBtmG9uF7uNbeiZoXT3TiRG8h\nah6z4Nnidhtj9jlyCSfjd0wJyGiLHjNnxexvU3kCgYAjT48sVk7z7h5pycwTBzOH\nDO4UOT5OcGWj0IURbpDjd8qkf8CbiK7ChG0QLAtOMAsI4lkfu58gsahrf7bNSQjy\nldb2BlCyZ+sHu7sAxWPk8DRsU4Alc3H+GQWgklnnjJZPwAapy1RIjyuoCNmKhAxm\nHpWgPSvIpZuvizu1ncSzew==\n-----END PRIVATE KEY-----\n""",
  "client_email": "service-account@aerial-antonym-444302-f9.iam.gserviceaccount.com",
  "client_id": "100259023955694299607",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40aerial-antonym-444302-f9.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# Google Sheets API認証を設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Googleスプレッドシートを開く
spreadsheet_id = "1eKhD929QC8fdvse2G92woknfWh7Dnv7Pmi2w1ZqXWCM"  # ★スプレッドシートのIDを入れる
sheet = client.open_by_key(spreadsheet_id).sheet1  # 1枚目のシートを選択

# スコア計算関数
def calculate_result(answers, label1, label2, label3):
    score_mapping = {
        "当てはまる": 2,
        "やや当てはまる": 1,
        "どちらでもない": 0,
        "あまり当てはまらない": -1,
        "当てはまらない": -2,
    }
    
    total_score = sum(score_mapping[ans] for ans in answers)

    # スコアが0の場合、最初の質問のスコアを参照
    if total_score == 0 and answers:
        first_answer_score = score_mapping.get(answers[0], 0)
        total_score = first_answer_score  # 最初の質問のスコアで決定

    if total_score > 0:
        return label1
    elif total_score < 0:
        return label2
    else:
        return label3

# Streamlit UI
st.title("性格診断アプリ")
st.write("各質問に対して「当てはまる」「当てはまらない」「どちらでもない」「やや当てはまる」「あまり当てはまらない」の中から選んでください。なお、(1)、(10)、(19)、(28)、(37)は、「どちらでもない」を選ばないでください")

# 質問
categories = {
    "カテゴリー1": [
        "(1)会場が遠くても積極的に遠征しに行くし、むしろモチベーションになっている", 
        "(2)SNSでたくさんの人と交流するのが楽しい", 
        "(3)イベントごと(コラボカフェ・ライブなど)が大好き。できればだれかと一緒に楽しみたい",
        "(4)推しの配信や投稿にコメントをするのが日課",
        "(5)SNSでグッズやチケットなどを積極的に交換している",
        "(6)Instagram等で推し活コミュニティを築いている",
        "(7)好きなキャラクターの誕生日は、生誕写真などを撮って盛大にお祝いする",
        "(8)同じジャンルの友達はたくさん欲しいし、仲良くしたい",
        "(9)ライブや演劇に参加したとき、隣の席の人に話しかける"
    ],
    "カテゴリー2": [
        "(10)推しの絶対的な味方でいたい",
        "(11)推しは近い存在でいてほしいが、夢をかなえる姿が見たいので、ビッグになってほしいと思う",
        "(12)推しに「がんばって」「好きだよ」と言われるだけでがんばれる",
        "(13)どんなヲタクとも仲良くなれる",
        "(14)推しがどんな秘密を抱えていても受け入れられると思う",
        "(15)まだ見つかっていないコンテンツを見つけて成長を見守るのが好き",
        "(16)推しではなくても人気芸能人の結婚報告に一喜一憂してしまう",
        "(17)5年以上推しているコンテンツがある",
        "(18)推しが何かがきっかけでバズったり、人気が上がったりすると自分のことのように嬉しい"
    ],
}

responses = []  # 初期化を追加

for category, questions in categories.items():
    for idx, q in enumerate(questions):
        col1, col2 = st.columns([2, 2])  # 質問とラジオボタンを横並びにする
        with col1:
            st.write(f"**{q}**")  # 質問を左に配置
        with col2:
            if idx in [0, 9, 18, 27, 36]:  # 特定の質問に対しては "どちらでもない" を除外
                response = st.radio(
                    "",
                    ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない"], 
                    key=f"{category}_{idx}", horizontal=True
                )  
            else:
                response = st.radio(
                    "",
                    ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない", "どちらでもない"], 
                    key=f"{category}_{idx}", horizontal=True
                )  
            responses.append(response)
            st.write(f"選択された回答: {response}")
        st.markdown("<br>", unsafe_allow_html=True)

if st.button("診断を実行"):
    st.session_state["responses"] = responses
    st.switch_page("free_questions.py")

# 自由記述ページ
if "responses" in st.session_state:
    st.title("自由記述アンケート")
    st.write("以下の質問に自由に回答してください。")
    
    free_responses = []
    questions = [
        "あなたが一番好きな推し活のエピソードを教えてください。",
        "推し活をしていて嬉しかったことは何ですか？",
        "推し活をしていて大変だったことは何ですか？"
    ]
    
    for i, question in enumerate(questions):
        response = st.text_area(f"{i+1}. {question}", key=f"free_response_{i}")
        free_responses.append(response)
    
    if st.button("診断を実行"):
        # 診断結果の計算
        final_result = (
            f"{calculate_result(responses[0:9], 'E', 'I', '意味が分からないばかり答えています')}"
            f"{calculate_result(responses[9:18], 'N', 'S', '意味が分からないばかり答えています')}"
            f"{calculate_result(responses[18:27], 'F', 'T', '意味が分からないばかり答えています')}"
            f"{calculate_result(responses[27:36], 'P', 'J', '意味が分からないばかり答えています')}"
            f"{calculate_result(responses[36:45], 'A', 'B', '意味が分からないばかり答えています')}"
        )
        
        # 現在の日付と時間を取得
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            sheet.append_row([now, final_result] + responses + free_responses)
        except Exception as e:
            st.error(f"スプレッドシートへの記録に失敗しました: {e}")
            st.stop()
        
        st.success(f"診断結果: {final_result}")
