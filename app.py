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

# Google API 認証
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(google_credentials), scope)
client = gspread.authorize(creds)

# Googleスプレッドシートを開く
spreadsheet_id = st.secrets["google_credentials"]["spreadsheet_id"]
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

# 結果ページの表示関数
def result_page():
    if "final_result" in st.session_state:
        st.title("診断結果")
        st.write(f"あなたの診断結果は: {st.session_state['final_result']}")
        # 必要に応じて、追加の結果やグラフを表示

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
    ]
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
    ]
    # 他のカテゴリーも追加可能
}

responses = []  # 回答のリスト

# 選択式質問の表示
for category, questions in categories.items():
    for idx, q in enumerate(questions):
        col1, col2 = st.columns([2, 2])  # 質問とラジオボタンを横並びにする
        with col1:
            st.write(f"**{q}**")  # 質問を左に配置
        with col2:
            options = ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない"]
            if idx not in [0, 9, 18, 27, 36]:  # 特定の質問以外は "どちらでもない" を追加
                options.append("どちらでもない")

            response = st.radio(
                "",
                options, 
                key=f"{category}_{idx}", horizontal=True
            )
            responses.append(response)

# **自由記述質問**
st.title("自由記述アンケート")
st.write("以下の質問に自由に回答してください。")

free_responses = []
free_questions = [
    "あなたが一番好きな推し活のエピソードを教えてください。",
    "推し活をしていて嬉しかったことは何ですか？",
    "推し活をしていて大変だったことは何ですか？"
]

for i, question in enumerate(free_questions):
    response = st.text_area(f"{i+1}. {question}", key=f"free_response_{i}")
    free_responses.append(response)

# 診断を実行
if st.button("診断を実行"):
    if len(responses) < 36:  # 質問が36個あるので、不足していればエラー
        st.error("全ての質問に回答してください")
        st.stop()

    # 診断結果の計算
    final_result = (
        f"{calculate_result(responses[0:9], 'E', 'I', '意味が分からないばかり答えています')}"
        f"{calculate_result(responses[9:18], 'N', 'S', '意味が分からないばかり答えています')}"
        f"{calculate_result(responses[18:27], 'F', 'T', '意味が分からないばかり答えています')}"
        f"{calculate_result(responses[27:36], 'P', 'J', '意味が分からないばかり答えています')}"
    )

    # 現在の日付と時間を取得
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Googleスプレッドシートに記録
    try:
        sheet.append_row([now, final_result] + responses + free_responses)
    except Exception as e:
        st.error(f"スプレッドシートへの記録に失敗しました: {e}")
        st.stop()

    # セッションに結果を保存
    st.session_state["final_result"] = final_result

    # 結果ページへ遷移するフラグを立てる
    st.session_state["result_page"] = True

# メイン処理
def main():
    if "result_page" in st.session_state and st.session_state["result_page"]:
        result_page()
    else:
        # 診断ページが表示されている場合
        st.write("診断を実行してください")

if __name__ == "__main__":
    main()
