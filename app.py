import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random

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

# セッションステートの初期化（エラー回避）
st.session_state.setdefault("final_result", None)
st.session_state.setdefault("result_page", False)
st.session_state.setdefault("diagnosis_id", None)  

# 診断結果を人間向けのラベルと説明文に変換する辞書
result_labels = {
    "INTP": ("株主", "株主タイプのあなた！特定の推しを影から支える株主さんは、物事を深く考える洞察力が備わっています。黙々と考えを巡らせる様子はまさに職人です。しかし推しに時間を費やしている分、何かあるとつい感情のコントロールが効かなくなってしまうことも？そんなときは一旦スマホから離れてみるのも1つの手かもしれません。")}

def result_page():
        """, unsafe_allow_html=True)


def calculate_result(answers, label1, label2, label3):
    score_mapping = {
        "当てはまる": 2,
        "やや当てはまる": 1,
        "あまり当てはまらない": -1,
        "当てはまらない": -2,
    }

    total_score = sum(score_mapping[ans] for ans in answers)

    if total_score == 0 and answers:
        total_score = score_mapping.get(answers[0], 0)

    if total_score > 0:
        return label1
    elif total_score < 0:
        return label2
    else:
        return label3

def diagnosis_page():
    st.title("性格診断アプリ")
    st.write("各質問に対して「当てはまる」「当てはまらない」「やや当てはまる」「あまり当てはまらない」の中から選んでください。")

    

    categories = {
        "カテゴリー1": ["(1)友達が好きなコンテンツは自分も手を出してみる",
        "(2)SNSでたくさんの人と交流するのが楽しい", 
        "(3)イベント事にはできればだれかと一緒に楽しみたい",
        "(4)誰かとコンテンツについての感想や思いを共有したい",
        "(5)推しのフォトスポットやカフェでグッズ・ぬい撮りをしたらSNSに上げたい",
        "(6)SNSでグッズを積極的に交換している", 
        "(7)好きなキャラクターの誕生日は、生誕写真などを撮ってお祝いする", 
        "(8)同じジャンルの友達はたくさん欲しいし、仲良くしたい", 
        "(9)行かないと決めていたイベントや買わないと思っていたグッズでも、第三者が参加を表明したり、購入したりしているのを見ると影響を受けてしまう。"],
        "カテゴリー2": ["(10)推しは1人ではなく、特定の2人をコンビで好きになることが多い",
        "(11)キャラクター同士の対比(性格や容姿など)を考えるのが好き",
        "(12)好きになる2人の関係性の形に譲れないこだわりがある(例：先輩後輩、犬猿の仲など)", 
        "(13)推しのことを考えるとき、いつもその隣には特定のキャラクターがいる(例：BなくしてAを語れない)", 
        "(14)推し単体でも好きだが、特定のコミュニティに所属して活動したり、共闘したりしている推しはもっと好き",
        "(15)推しの行動に対して、すぐ他のキャラクターと結び付けて考えてしまう(例：Ａのこの行動を見たＢはどう思うだろう？など)", 
        "(16)キャラクター同士の関係性に対して自分なりの解釈がある", 
        "(17)グッズを買うなら推しだけではなく、推しと関係性が深い子や推しの相棒とコンビで買いたいと思う", 
        "(18)推している2人が同じ画の中にいるとテンションが上がる"],
        "カテゴリー3": ["(19)推しコンテンツに否定的な感情を抱くことがほとんどない", 
        "(20)他の人の意見が解釈違いだったり、自分は思いもしなかった感想だったりしても受け入れられる", 
        "(21)コンテンツの変化には付いていける方だ", 
        "(22)自分とはタイプの違うオタクとも仲良くなれる自信がある", 
        "(23)推しにどんな一面があっても受け入れられると思う", 
        "(24)流行っているコンテンツには積極的に足を踏み入れる", 
        "(25)いわゆる王道と呼ばれるものが好き", 
        "(26)5年以上変わらず好きなコンテンツがある", 
        "(27)推しや好きなコンテンツがバズったり、人気が上がったりすると自分のことのように嬉しい"],
        "カテゴリー4": ["(28)合言葉「来月の自分が頑張る」を唱えながらクレジットカードを使う",
        "(29)推しのための時間は惜しまない、または惜しむという概念がない",
        "(30)グッズ購入や課金など推しのためにたくさん貢献している人を見て、自分もそうなりたいと思う",
        "(31)周りに「同じじゃない？」と言われるようなグッズでもついつい買ってしまったり、同じグッズを何個も集めたりする", 
        "(32)自分の知らない推しの情報を相手が知っていると悔しい",
        "(33)寝てる時を除けばずっと推しのことを考えているといっても過言ではない",
        "(34)入金してから時間が経ってからグッズが届いたりイベント当日を迎えたりするので、そのときは実質無料である", 
        "(35)推しコンテンツの最新情報は見逃したくないのでチェックを欠かさない", 
        "(36)グッズが届いても何を買ったか覚えていない"]
    }

    responses = []
    for category, questions in categories.items():
        for idx, q in enumerate(questions):
            st.write(f"**{q}**")
            options = ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない"]
    
    # 名前入力欄
    name = st.text_input("お名前を入力してください", key="name")
            
    if st.button("診断を実行"):
        # 名前が入力されていない場合、エラーを表示して中断
        if not st.session_state["name"]:
            st.error("お名前を入力してください。")
            return
            
        if len(responses) < 36:
            st.error("全ての質問に回答してください")
            return

        final_result = (
            f"{calculate_result(responses[0:9], 'E', 'I', '意味が分からない')}"
            f"{calculate_result(responses[9:18], 'S', 'N', '意味が分からない')}"
            f"{calculate_result(responses[18:27], 'F', 'T', '意味が分からない')}"
            f"{calculate_result(responses[27:36], 'P', 'J', '意味が分からない')}"
        )

        # 診断結果番号を生成
        diagnosis_id = random.randint(10000000, 99999999)
        st.session_state["diagnosis_id"] = diagnosis_id

        # スプレッドシートに名前と診断結果番号を記録
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([now, st.session_state["name"], diagnosis_id, final_result] + responses)
        
        st.session_state["final_result"] = final_result
        st.session_state["result_page"] = True
        st.rerun()

def main():
    if st.session_state.get("result_page", False):
        result_page()
    else:
        diagnosis_page()

if __name__ == "__main__":
    main()
