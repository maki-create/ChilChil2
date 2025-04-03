import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        .question {
            margin-bottom: 300px;  /* 質問と質問の間隔を詰める */
        }
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
    "ENFP": ("カリスマ", "カリスマタイプのあなた！推しに一途で寝ても覚めても生活が推し一色なカリスマさん。周りを圧倒するほどの行動力とパワーを持ち合わせています。基本的に全肯定タイプですが、それゆえに気づいたら口座残高が一桁減っている……なんてことも⁉ 一度お財布の紐をぎゅっと結んでみてもいいかもしれません。"),
    "ESFJ": ("支援者", "支援者タイプのあなた！友好的な支援者さんの周りには、同じく陽気なオタク仲間さんが多いはず。どちらかというとニコイチ・サンコイチが好きな支援者さんは、みんなの関係性を見守る壁ポジションです。私生活を優先できるしっかり者ですが、ダメージには鈍感かも？辛いことがあったら無理せず休んでね。"),
    "INFP": ("ユートピアン", "カリスマタイプのあなた！推しに一途で寝ても覚めても生活が推し一色なカリスマさん。周りを圧倒するほどの行動力とパワーを持ち合わせています。基本的に全肯定タイプですが、それゆえに気づいたら口座残高が一桁減っている……なんてことも⁉ 一度お財布の紐をぎゅっと結んでみてもいいかもしれません。"),
    "ISFP": ("愛好家", "愛好家タイプのあなた！基本的には1人で推し活をしていますが、心根は元気なのでいろいろな人と仲良くなれる素質があります。大好きな推しや、愛してやまないコンビのためにお金も時間も惜しみませんが、ややチョロすぎる気配が。悪い人に騙されないように気をつけながら推し活を楽しんで！"),
    "ENTP": ("啓蒙者", "啓蒙者タイプのあなた！ 日夜推しのことを考えたり、友達に推しのことを語ったりするのが大好きな啓蒙者さんはまさに知識の源泉。推しに対して確固たる信念と、それを語れる強さを持っています。ただ、時折推しに対して独占欲を暴走させてしまうことも……？ 時にはブレーキの点検も忘れずにね。"),
    "INTJ": ("理想主義者", "理想主義者タイプのあなた！推しに対して無限の愛を注ぐ理想主義者さんは、自分にも他人にもストイック。推しを原動力に自分にも投資できる努力家さんです。しかし複雑な想いを隠すためつい1人引きこもってしまいがち……？ 信頼できる人を見つけて共有してみてね"),
    "ESFP": ("デザイナー", "デザイナータイプのあなた！推し活に関するセンスが抜群のデザイナーさん。自分にとって楽しいオタ活を設計するのが上手で、理想の関係性を求めて目を鋭く光らせています。推しだけでは物足りず、つい他のキャラクターのグッズを集めてしまうコレクター気質な一面も。収納スペースが確保できるようなオタ活デザインもしてみてね。"),
    "ISTJ": ("フォロワー", "フォロワータイプのあなた！応援している推しや、好きなコンビ(もしくはグループ)が存在していますが、基本的に誰かに打ち明けることはなくひっそりと楽しんでいます。現実的であるが故に冷静なフォロワーさんですが、無自覚のうちに行き場のない感情を持て余してしまうことも……？一度感情を昇華する場所を探してみてもいいかもしれません。"),
    "INFJ": ("保護者", "保護者タイプのあなた！推しの幸せを願いひっそり応援する平和主義者な保護者さん。私生活のあれそれをこなしながら時折推しで癒される、メリハリのあるタイプです。しかし推しのすべてを肯定してしまうので、モヤモヤしても何とか許してしまうことも？ダメと言う勇気も大切にしましょう！"),
    "ISTP": ("研究者", "研究者タイプのあなた！推しや好きな関係性の2人の分析を怠らない研究者さんは、黙々と情報を集める能力に長けています。やろうと思えば自給自足も可能な研究者さんですが、たまに人の意見や解釈が欲しくなってしまいそう？交流の輪を広げてみると、新たな推しが見えてくる……かもしれません。"),
    "ENTJ": ("演出家", "演出家タイプのあなた！ お財布と時間に余裕があればオタ活に勤しむフットワーク軽めの演出家さん。楽しいことが大好きですが、行き過ぎないように踏みとどまれる理性もある賢い一面もあります。推しを真っすぐ見つめる演出家さんは、推しが不遇になってしまうとダメージを受けてしまうかも……？ 1人で抱え込まず、周りのオタク友達に相談してみましょう！"),
    "ISFJ": ("マネージャー", "マネージャータイプのあなた！好きなものを好きなだけゆったり推すマネージャーさん。人の意見も柔軟に取り入れられますが、結局は原作に行き着く原点回帰型オタクさんです。マイペースなマネージャーさんですが、ちょっぴり刺激が足りないこともありそう？ たまには新たな世界に飛び込んでみよう！"),
    "ENFJ": ("リーダー", "リーダータイプのあなた！ 友達とワイワイ推し活をすることが好きで、推しによって人生が彩られているリーダーさん。基本的に推しだけを愛で、応援の声を届ける一途で平和なオタ活を好みます。基本的に誰とでも仲良くなれるタイプのリーダーさんですが、平和主義ゆえ他のオタクさんとの熱量の差に悩んでしまうかも……？ たまには1人でのんびりしてみるのもいいかもしれません。"),
    "ESTJ": ("思想家", "思想家タイプのあなた！大好きなあの2人(またはグループ)について日々考えている思想家さんの脳内は、まるで哲学書のように分厚くなっていることも多いはず。周りには異なる推しを持ちつつ思想は同じオタクさんがいるのではないでしょうか？ ただ解釈に全力投球なので、自分と違う感想にモヤモヤしてしまうことも……？ たまには別のコンテンツに触れてリフレッシュしてみてね。"),
    "ESTP": ("投資家","投資家タイプのあなた！推しているコンビ(もしくはグループ)について譲れない解釈がある投資家さん。より奥深く知るために供給を反芻しているので、一度推し語りを始めると止まりません。推しのために使うお金はご祝儀気分！しかし自分の限界を突破してしまうこともあるので、資金管理も大切にしましょう。"),
    "INTP": ("株主", "株主タイプのあなた！特定の推しを影から支える株主さんは、物事を深く考える洞察力が備わっています。黙々と考えを巡らせる様子はまさに職人です。しかし推しに時間を費やしている分、何かあるとつい感情のコントロールが効かなくなってしまうことも？そんなときは一旦スマホから離れてみるのも1つの手かもしれません。")}

def result_page():
    # 'name'がセッションに保存されているかチェック
    if 'name' not in st.session_state or not st.session_state['name']:
        st.error("名前を入力してください。")
        return

    final_result = st.session_state["final_result"]
    result_name, result_description = result_labels.get(final_result, ("診断結果不明", "該当する診断結果が見つかりませんでした。"))

    # 診断結果番号を生成
    diagnosis_id = st.session_state["diagnosis_id"]
    
    st.title("診断結果")
    st.write(f"あなたの診断結果は: **{result_name}**")
    st.write(f"**{result_description}**")

    st.write(f"診断結果番号: {diagnosis_id}")

    google_form_url = (
        f"https://docs.google.com/forms/d/e/1FAIpQLScnQ2px9H6bBa_oFc1J1L0CwFBpwqjx9Lx8PtzpTEYWdlG04w/viewform?"
        f"usp=pp_url&entry.1420480324={st.session_state['name']}"
        f"&entry.1395543321={diagnosis_id}"
        f"&entry.1270609001={result_name}"
    )


    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 30px;">
            <a href="{google_form_url}" target="_blank">
                <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; cursor:pointer;">
                    アンケートに進む
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        """
        <div style="text-align: center; margin-top: 30px;">
            <a href="https://chilchil2-qxehnzkrhvqchpqqgjsgum.streamlit.app/" target="_blank">
                <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; cursor:pointer;">
                    元のページに戻る
                </button>
            </a>
        </div>
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
    st.write("各質問に対して「当てはまる」「やや当てはまる」「あまり当てはまらない」「当てはまらない」の中から選んでください。")

    

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
           
            response = st.radio("", options, key=f"{category}_{idx}", horizontal=True)
            responses.append(response)
            
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
