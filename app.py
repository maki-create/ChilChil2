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

# Googleスプレッドシートを開く（シートのURLまたはIDを指定）
spreadsheet_id = "1eKhD929QC8fdvse2G92woknfWh7Dnv7Pmi2w1ZqXWCM"  # ★スプレッドシートのIDを入れる
sheet = client.open_by_key(spreadsheet_id).sheet1  # 1枚目のシートを選択

# スコア計算関数（スコアルール変更）
def calculate_result(answers, label1, label2, label3):
    score_mapping = {
        "当てはまる": 2,
        "やや当てはまる": 1,
        "あまり当てはまらない": -1,
        "当てはまらない": -2,
        "どちらでもない": 0,
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
     "IかEか": [
                "(1)会場が遠くても積極的に遠征しに行くし、むしろモチベーションになっている", 
                "(2)SNSでたくさんの人と交流するのが楽しい", 
                "(3)イベントごと(コラボカフェ・ライブなど)が大好き。できればだれかと一緒に楽しみたい",
                "(4)推しの配信や投稿にコメントをするのが日課",
                "(5)SNSでグッズやチケットなどを積極的に交換している",
                "(6)Instagram等で推し活コミュニティを築いている",
                "(7)好きなキャラクターの誕生日は、生誕写真などを撮って盛大にお祝いする",
                "(8)同じジャンルの友達はたくさん欲しいし、仲良くしたい",
                "(9)ライブや演劇に参加したとき、隣の席の人に話しかける"],
     "カテゴリー2": ["(10)推しの絶対的な味方でいたい",
                "(11)推しは近い存在でいてほしいが、夢をかなえる姿が見たいので、ビッグになってほしいと思う",
                "(12)推しに「がんばって」「好きだよ」と言われるだけでがんばれる",
                "(13)応援を形にして残したいので、CD、グッズを買いたいし、できれば同じ価値観の人と仲良くなりたい",
                "(14)推しがどんな秘密を抱えていても受け入れられると思う"
                ,"(15)まだ見つかっていないコンテンツを見つけて成長を見守るのが好き"
                ,"(16)推しではなくても人気芸能人の結婚報告に一喜一憂してしまう"
                 ,"(17)5年以上推しているコンテンツがある"
                ,"(18)推しが何かがきっかけでバズったり、人気が上がったりすると自分のことのように嬉しい"],
     "カテゴリー3": ["(19)友達と推しが同じだったら嬉しい",
                "(20)好きなものができたら周りに言いたいし、ハマってくれたら嬉しい",
                "(21)興味を持った作品についてほかの読者の意見をみたくなる",
                "(22)推しや作品に対して考察をしたり、それを誰かと共有したりするのが好き",
                "(23)推しのグッズ制作、手芸を始める",
                "(24)Xなどの流行に敏感で、隙あらば推しと絡めて考えたくなる",
                "(25)気持ちが昂ると創作をしたくなる",
                "(26)推しのことを深く知るために勉強をする",
                "(27)推しがプロモーションを担当しているアイテムを積極的に購入したり、周りに勧めたりする"],
     "カテゴリー4": ["(28)合言葉は「来月の自分が頑張る」と言いながらクレジットカードを使う",
                "(29)推しのためなら時間やお金を惜しまない",
                "(30)グッズ購入や観劇など推しのためにたくさん貢献している人を尊敬する",
                "(31)周りに「同じじゃない？」と言われるようなグッズでもついつい買ってしまう",
                "(32)とても多忙な状況でも、チケットが当たったら迷わず現場に行く",
                "(33)遠征に行くとき、ついつい前日や当日にパッキングをしてしまうことがある",
                "(34)入金したから時間が経ってからグッズが届いたりイベント当日を迎えたりするので、そのときは実質無料である"
                ,"(35)どんな推しでも見逃したくないのでチェックを欠かさない",
                "(36)グッズが届いても何を買ったか覚えていない",],
    "カテゴリー5": ["(37)少年漫画が好きだ",
                "(38)色々な世界線の推しが見てみたい",
                "(39)推しに壮絶な過去があると燃える",
                "(40)実は周りに言えないニッチな趣味を持っている",
                "(41)ミュージカルや映画を見て役を好きになっても、演じている本人を深堀りすることはない",
                "(42)メインキャラよりサブキャラに興味をもってしまうほうだ",
                "(43)ドラマや映画を見るとき、映像のクオリティよりキャラ同士の関係性を目で追ってしまう"
                ,"(44)推しの概念ソングを探したり、誕生日の花言葉をついつい調べてしまう",
                "(45)推しが有終の美を飾り物語から退場してしまうことがよくある",]
                
}

responses = []  # 初期化を追加

for category, questions in categories.items():
    for idx, q in enumerate(questions):
        col1, col2 = st.columns([2, 2])  # 質問とラジオボタンを横並びにする
        with col1:
            st.write(f"**{q}**")  # 質問を左に配置
        with col2:
            response = st.radio("", ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない", "どちらでもない"], 
                                key=f"{category}_{idx}", horizontal=True)  
            responses.append(response)

        # 質問と質問の間に改行を入れる
        st.markdown("<br>", unsafe_allow_html=True)  

if st.button("診断を実行"):
    st.session_state["final_result"] = (
        f"{calculate_result(responses[0:9], 'E', 'I', '意味が分からないばかり答えています')}"
        f"{calculate_result(responses[9:18], 'N', 'S', '意味が分からないばかり答えています')}"
        f"{calculate_result(responses[18:27], 'F', 'T', '意味が分からないばかり答えています')}"
        f"{calculate_result(responses[27:36], 'P', 'J', '意味が分からないばかり答えています')}"
        f"{calculate_result(responses[36:45], 'A', 'B', '意味が分からないばかり答えています')}"
    )
    
    final_result = st.session_state["final_result"]  # ローカル変数に保存

    if "意味が分からない" in final_result:
        st.warning("(1)、(10)、(19)、(28)、(37)は、「どちらでもない」を選ばないでください")
    else:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            sheet.append_row([now, final_result[0], final_result[1], final_result[2], final_result[3], final_result] + responses)
        except Exception as e:
            st.error(f"スプレッドシートへの記録に失敗しました: {e}")
            st.stop()

        st.switch_page(f"pages/{final_result}.py")
