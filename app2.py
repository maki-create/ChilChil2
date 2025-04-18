import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import random

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        .question {
            margin-bottom: 5px;  /* カテゴリーの見出しと次の項目の間隔を狭くする */
        }
        .radio-group {
            margin-top: 0px !important;  /* ラジオボタンの上のスペースを詰める */
            margin-bottom: 0px !important;  /* ラジオボタンの下のスペースを詰める */
        }
        .stRadio {
            margin-top: -40px !important;
            margin-bottom: 20px !important;  /* ラジオボタンの間隔を縮める */
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
    "ENFP": ("カリスマ", "推しに一途で、寝ても覚めても生活が推し一色のカリスマさん。周りを圧倒する行動力とパワーの持ち主です。推しやオタク仲間に対していつも肯定的かつ、広い心で接する温かさが魅力。「推しの顔が良すぎて困る」と嘆きつつ、推しの応援に全力投球するのが推し活スタイルです。その結果、気づけば口座残高が一桁減っている……なんてことも⁉ 常に金欠状態なので非オタクからはお金の使い方について呆れられ、同じオタクからさえ「ビビる」と言われるほどの情熱家。「お花畑オタク」といわれることもありますが、そんな苦言を活力に変えてしまうポジティブさが特徴。超マイペースに楽しくオタク生活を謳歌しており、推しへの貢ぎ方には尊敬の念を向けているオタクが近くにいるかもしれません！口座残高と向き合いつつこれからもオタク街道を突き進んでください。"),
    "ESFJ": ("支援者", "特定の2人の関係性に魅力を感じる支援者さんは柔軟なカプ推し。ニコイチな2人が大好きで、セットでの登場に喜びます。「2人が幸せならなんでもいい！」が口癖で、公式の展開や他オタクとの解釈違いはあまり気にしません。みんなの関係性を見守る「壁ポジション」として、周囲には同じく平和を愛するオタク仲間が集まりやすいでしょう。推しコンテンツには穏やかなストーリーを求めますが、万が一推しカプが悲しい結末を迎えても、転生IFや現代IFなど別の形で2人を幸せにできるくらい想像力も豊かです。現実主義者として私生活を優先できるしっかり者ですが、時に自分へのダメージに鈍感なところもあるので、辛いときは休息も大切に！"),
    "INFP": ("ユートピアン", "推しのすべてを愛し、かつ妄想に忙しいユートピアンさん。一度考え込むと止まらない集中力で、寝る前のブクマや推し関連タグの徘徊に没頭します。どんなに翌日の予定が詰まっていても、この大切な時間だけは削れず、丑三つ刻を過ぎてもネットをさまよいがち。特に金曜の夜は、この世で一番好きな「妄想タイム」で「推しと結婚できないけど結婚できる」といった幻想に身を任せることも。推しに貢献している自負はありますが、自分以上に推しに貢いでいるオタクを密かに気にしてしまうことも。繊細な心の持ち主なので、他のオタクの言動で思わぬダメージを受けてしまうことがありますが、時には自分を甘やかしながら、推しとの素敵な妄想の世界を楽しんでくださいね！"),
    "ISFP": ("愛好家", "SNSを徘徊中に見つけたファンアートや切り抜き動画からうっかり沼にハマる傾向がある愛好家さん。元気なオタクの心を持ち、自分からは行動しなくても話しかけられると熱く語り出す情熱の持ち主です。「好きってわけじゃないんだけど…」と最初は言い訳しつつも、数か月後には立派な「沼の地底人」になることも。最初の沼落ちのきっかけの推しと今の推しは大抵別の人。指数関数的に「沼が増える」典型的なタイプですが、自分の沼が不穏な空気になると別の沼に避難する賢さも持ち合わせています。推しと公式へのお金は惜しみないので、悪い人に騙されないよう気をつけながら、これからも様々な沼を渡り歩く楽しい推し活を続けてくださいね！"),
    "ENTP": ("啓蒙者", "日夜推しのことを考え、友達に熱く語るのが大好きな啓蒙者さん。「あくまで私の解釈ですが」と謙虚に言いながらも、推しへの深い理解に基づいた持論を堂々と展開する姿は、多くの仲間から共感を集め、いつの間にかオタク界隈の世論をまとめるリーダー的な存在になることも。揺るぎないその情熱的な推し語りがときに鋭い切り口となり、思いがけず熱い議論の中心になることもあるので、時には冷静さを取り戻す瞬間も大切にしてくださいね。ときに推しに対して厳しい意見を口にしたり、毒を吐いてしまうこともありますが、それは愛情ゆえのことであり、定期的な気持ちの確認手段のようなもの。それでもやっぱり「大好き！」という想いが最後にはすべてを包み込み、推しの活躍や知名度の上昇を心から喜び、祝福することができるのです。"),
    "INTJ": ("理想主義者", "ひっそり無限の愛を推しに注ぐ理想主義者さん。「推しの隣に並んでも恥ずかしくない自分になりたい」という思いが、勉強や仕事、ダイエットなど様々な面での原動力に。自分では「お金をかけていない」と思っていても、実は知らず知らずのうちに株主レベルの投資を推しと自己につぎ込んでいます。同担拒否の傾向があり、他のオタクの推し活スタイルに対して密かに思うところがあるため、あえて一人の時間を大切している側面も。長年推しに一途なこともあり、ふとした瞬間に「そろそろ私と推しが結ばれてもいいよな…」と思うロマンチストでもあります。向上心あふれるストイックな努力家さん、あなたの愛の叫びを聞きたがっている仲間が周りに潜んでいるはず！思いを共有してみるともっと楽しい推し活ができるかも⁉"),
    "ESFP": ("デザイナー", "収集家気質で消費意欲旺盛なデザイナーさん。推しグッズは必ず両方同数購入。欲しいと思っていなかったグッズでも周りの人が持っていると欲しくなり、推しキャラ以外のキャラクターのグッズも集めてしまう徹底したコレクター気質があります。 イメージソングを熱唱し、推し概念○○を探しだし、生活空間のすべてを推しで彩ろうとする姿勢は、まさに「死ぬほどオタクで死ぬほどオシャレ」。推しカプへの信念は強く、原作で二人が不幸な結末を迎えても「来世で幸せにさせる、俺が！」と豊かな想像力で、新たな物語を紡ぎ出しオタクから称賛されます。コミュニティ内での自分の立ち位置を理解しているので、その役割を果たすことに生きがいを感じています。"),
    "ISTJ": ("フォロワー", "一見非オタクと見紛うほど一般人に同化しているフォロワーさん。推しのことは心から大好きですが、いわゆる「推し活の経済戦争」には参加するような無理はしません。「公式」と名のつく情報源には惜しみなく投資する研究者気質の一面を見せることも。一日の終わりに自分の解釈を深め、妄想に浸る時間を何よりも大切にしています。ひっそりと一人で推し活を楽しむスタイルは心地よいのですが、時に無自覚のうちに行き場のない感情を持て余してしまうことも……？鍵アカウントで行き場のない気持ちを吐き出し感情を昇華することは、心の安定につながることでしょう。情報収集と妄想の世界で、これからも理想的な推し活を楽しんでください！"),
    "INFJ": ("保護者", "私生活と推し活を苦労なく両立させる保護者さん。推しに対して余計な疑念がないので、推しを効率よく摂取でき短時間で質の高い癒しを得られます。忙しい日々の中でも「〇〇くん可愛い」と心の中で一回つぶやくだけで疲れが吹っ飛ぶ回復力の持ち主です。こうした推し活スタイルは、時に熱量の高いオタクから疎まれることもありますが、いわば理想的なオタク生活の完成型。意図せず推し活の高みにたどり着ける才能を持っていたのです。自身の推し活スタンスについて他のタイプのオタクと比べる必要はありません！これからもオタク・ライフ・バランスを大切に、あなたなりのオタ活を楽しんでください"),
    "ISTP": ("研究者", "情報収集と深い解釈にこだわる研究者さん。一つの沼を深く掘り下げて源泉を見つけることに喜びを感じるタイプ。誰も気づかないような発言の意図や伏線、裏設定まで知り尽くしたいという強い探究心を持ち、推しの好きな物ならなんでも興味が湧きます。そのため推しの範囲を超えた追及が他ジャンルでも始まるので、結果的に多方面に精通することに。「他人と解釈が合わなければ自分で作ってしまえばいい」と創作意欲も旺盛です。また経済戦争にもひっそりと参加し、推しのSSR（スーパー・スペシャル・レア）をそろえるためなら課金も厭いません。自給自足可能な研究者さんですが、仲間と意見交換しあうことで新たな推しの魅力が見えてくるかもしれませんね！"),
    "ENTJ": ("演出家", "楽しいことに目がなくフットワークが軽い演出家さん。お財布と時間に余裕があれば、お友達同士でワイワイオタ活を楽しみます。交友関係が広く、多くのイベントに誘われる人気者なので、推し活ダブルブッキングを回避しながら今日もイベントに向かいます。一人の推しを真っすぐ見つめ応援することで大きな充実感を得られます。ただ推しの不遇にダメージを受けやすいことも。また推し活の中で、お金の使い方など考え方の違いでモヤモヤしたり、同担にはちょっとした警戒心を抱きがちなところも。推しを通してつながった友達は人生の大きな財産です。そんな時は一人で抱え込まず、信頼できるオタク友達に相談してみましょう。"),
    "ISFJ": ("マネージャー", "好きなカップリングをゆったりと推すマネージャーさん。ひっそりと一人で推し活を楽しみ、自分であれこれ考え様々な解釈を漁りはするものの、最終的には原作に帰結する原点回帰型のオタクです。人の意見も柔軟に取り入れられます。通勤時間や寝る前の癒しとして推しが存在し、ストーリーを読むのが何より好きなのですが、基本課金はしないというスタンスです。派手なお金使いをしないので一般人に見られがちですが、脳内はしっかりオタクだったりします。揉め事が苦手なのでひっそりと平和に無理のない推し活が心地よいのですが、ときに刺激不足に感じることも。そんなとき新たな世界に飛び込んでみると、きっと違った楽しみが待っているはずです！"),
    "ENFJ": ("ムードメーカー", "友達とワイワイ推し活をすることが大好きで、推し活が人生に彩りを添えている社交的なムードメーカーさん。基本的に推し一人を純粋に愛で、応援の声を届ける一途で平和なオタ活を好む優しいオタクです。同担拒否もあまりなく、誰とでも分け隔てなく仲良くなれる包容力があり、どんな推しでも基本的に受け入れる広い心を持っています。運営に対しても不満をあまり持たない穏やかな姿勢が特徴的です。推しのことが大好きで同じオタク友達とも平和なコミュニティを作る才能があるリーダーさんですが、周りの人にやや流されやすい一面もあるかも……ムードメーカーさんはマイペースに推し活をしているので気にすることは少ないかもしれませんね。これからもあなたらしい推し活を続けていってください！"),
    "ESTJ": ("思想家", "大好きな推し、または推しカプ（またはグループ）の関係性について日々考えを巡らせる思想家さん。その脳内は、まるで分厚い哲学書のように深い考察で満ちています。推し活は一人よりも誰かと共有したいタイプですが、オタク友達の条件はやや厳しめかも。推しには自分なりの確固たる解釈があるため、それと合わないオタクとは初めから距離を置く現実的な一面も。周囲の友人は同じような価値観を持つ人が多く、金銭感覚や解釈面でも揉めることは少ないでしょう。グッズ購入は自分の欲しいと思ったものを吟味して買うタイプ。推しコンテンツのイベントにも頻繁には通わないものの、大事なイベントや気の合う仲間との交流は大切にしています。たまには別のコンテンツや仲間に触れてリフレッシュするのもいいかもしれませんね！"),
    "ESTP": ("投資家","カップル推し（またはグループ推し）が多い投資家さん。推しを深く理解するため常に供給を反芻するため、関係性の解釈に揺るぎない信念を持っています。その思いを伝えるために時間とお金を使うことを厭いません。カップル推しがメインなので、当然ながら投資金額が倍増。また推しの幸せのためなら「ご祝儀」気分で簡単に追加投資してしまいます。結果なんでこんなに出費多いんだろう…？と大真面目に考えることも。お金は使っているのではなく自然と出て行ってしまう感覚です。 とはいえ推し活で得られる充実感は望外なリターン。自分の限界を突破することがないように資金管理を大切に楽しいオタ活ライフを♪"),
    "INTP": ("株主", "推しをひっそり見守り支える株主さん。物事を深く考える洞察力があり、推しの将来について黙々と考えを巡らせる参謀のような存在です。これまで投資したお金は株主総会での議決権。推しが納得できない扱いを受けると運営に権利の行使を申し出ることも。持ち株数が他のオタクとはゼロ一つ違うのですが、自分以上に投資している猛者を常に見ているため感覚の差に気づいていないかも。一途で熱量も無尽蔵なため、推しが自分の理想と違う方向性に向いてしまうと深刻なメンタルブレイクを起こす不安もあります。ただ推しへの深い愛情と献身は、他のオタクにはない素晴らしい能力。日々自分をケアする方法を増やしてサステナブルオタ活をエンジョイしましょう。")}

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
        f"https://docs.google.com/forms/d/e/1FAIpQLSe3HaEvt8A206-25CSmJMUPeqUd3tD74xgEBoijslLVEu4Wzg/viewform?usp=dialog"
        f"usp=pp_url&entry.186198495={diagnosis_id}"
        f"&entry.1966712441={result_name}"
        f"&entry.1541743808={st.session_state['name']}"
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

   #  st.markdown(
       #  """
        # <div style="text-align: center; margin-top: 30px;">
            # <a href="https://chilchil2-qxehnzkrhvqchpqqgjsgum.streamlit.app/" target="_blank">
              #   <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; cursor:pointer;">
                   #  元のページに戻る
                # </button>
           #  </a>
       #  </div>
       #  """, unsafe_allow_html=True)


def calculate_result(answers, label1, label2, label3):
    score_mapping = {
        "とても当てはまる": 2,
        "やや当てはまる": 1,
        "あまり当てはまらない": -1,
        "まったく当てはまらない": -2,
    }

    total_score = sum(score_mapping.get(ans, 0) for ans in answers)

    if total_score == 0 and answers:
        count_positive = answers.count("とても当てはまる")
        count_negative = answers.count("まったく当てはまらない")
        
        if count_positive > count_negative:
            return label1
        elif count_negative > count_positive:
            return label2
        else:
            return label3
    else:
        if total_score > 0:
            return label1
        elif total_score < 0:
            return label2
        else:
            return label3


def diagnosis_page():
    st.title("オタクタイプ診断")
    st.write("各質問に対して「とても当てはまる」「やや当てはまる」「あまり当てはまらない」「まったく当てはまらない」の中から選んでください。")
    st.write("※選択操作を素早く行いすぎるとエラーが発生する場合がございます。恐れ入りますが、エラーが発生した際はページをリロードのうえ、ゆっくりとご操作いただきますようお願い申し上げます。")

    

    categories = {
        "カテゴリー1": ["(1)友達が好きなコンテンツは自分も手を出してみる",
        "(2)SNSのリプでやり取りをよくする", 
        "(3)イベント事にはできればだれかと一緒に楽しみたい",
        "(4)誰かとコンテンツについての感想や思いを共有したい",
        "(5)好きなジャンルの話ができる人が周りにいないときはネットで探す",
        "(6)気になるイベントがあっても同行者が見つからなければ行かない", 
        "(7)好きなキャラクターの誕生日は、生誕写真などを撮ってお祝いする", 
        "(8)同じジャンルの友達はたくさん欲しいし、仲良くしたい", 
        "(9)行くつもりがなかったイベントでも友達に誘われたら行く"],
        "カテゴリー2": ["(10)推しは1人ではなく、特定の2人をコンビで好きになることが多い",
        "(11)キャラクター同士の対比(性格や容姿など)を考えるのが好き",
        "(12)推しの相棒や推しと関係性が深い人がいるとその人もセットで好きになりやすい", 
        "(13)推しのことを考えるとき、いつもその隣には特定のキャラクターがいる(例：BなくしてAを語れない)", 
        "(14)推し単体でも好きだが、特定のコミュニティに所属して活動したり、共闘したりしている推しはもっと好き",
        "(15)推しの行動に対して、すぐ他のキャラクターと結び付けて考えてしまう(例：Ａのこの行動を見たＢはどう思うだろう？など)", 
        "(16)キャラクター同士の関係性に対して自分なりの解釈がある", 
        "(17)推し単体でも大好きだが、推しが仲の良い人と一緒にいるといつもより幸福感が増す", 
        "(18)推している2人が同じ画の中にいるとテンションが上がる"],
        "カテゴリー3": ["(19)推しコンテンツに否定的な感情を抱くことがほとんどない", 
        "(20)他の人の意見が解釈違いだったり、自分は思いもしなかった感想だったりしても受け入れられる", 
        "(21)コンテンツの変化には付いていける方だ", 
        "(22)自分とはタイプの違うオタクとも仲良くなれる自信がある", 
        "(23)推しがイメージとは違う言動をしても好きでいられる自信がある", 
        "(24)流行っているコンテンツには積極的に足を踏み入れる", 
        "(25)いわゆる王道と呼ばれるものが好き", 
        "(26)推し活特集のような投稿や記事が好きである", 
        "(27)推しや好きなコンテンツがバズったり、人気が上がったりすると自分のことのように嬉しい"],
        "カテゴリー4": ["(28)合言葉「来月の自分が頑張る」を唱えながらお金を使う",
        "(29)推しのための時間は惜しまない、または惜しむという概念がない",
        "(30)グッズ購入や課金など推しのためにたくさん貢献している人を見て、自分もそうなりたいと思う",
        "(31)周りに「同じじゃない？」と言われるようなグッズでもついつい買ってしまったり、同じグッズを何個も集めたりする", 
        "(32)自分の知らない推しの情報を相手が知っていると悔しい",
        "(33)寝てる時を除けばずっと推しのことを考えているといっても過言ではない",
        "(34)お金を払ったあと時間が経ってからグッズが届いたりイベント当日を迎えたりするので、そのときは実質無料である", 
        "(35)推しコンテンツの最新情報は見逃したくないのでチェックを欠かさない", 
        "(36)グッズが届いても何を買ったか覚えていない"]
    }

    responses = []
    for category, questions in categories.items():
        for idx, q in enumerate(questions):
            st.write(f"**{q}**")
            options = ["とても当てはまる", "やや当てはまる", "あまり当てはまらない", "まったく当てはまらない"]
           
            response = st.radio("", options, key=f"{category}_{idx}", horizontal=True)
            responses.append(response)
            
    # 名前入力欄
    name = st.text_input("お名前（ちるちるユーザー名）を入力してください", key="name")
            
    if st.button("診断を実行"):
        # 名前が入力されていない場合、エラーを表示して中断
        if not st.session_state["name"]:
            st.error("お名前（ちるちるユーザー名）を入力してください")
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
