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

# セッションステートの初期化（エラー回避）
st.session_state.setdefault("final_result", None)
st.session_state.setdefault("result_page", False)

# 診断結果を人間向けのラベルと説明文に変換する辞書
result_labels = {
    "ENFP": ("カリスマ", "あなたはカリスマ性があり、周囲の人を引きつける魅力を持っています。自信を持ち、積極的に行動することでさらに成長できます。"),
    "ES": ("エネルギッシュ", "あなたは活発でエネルギッシュな性格です。常に新しいことに挑戦し、周囲を巻き込んで楽しむタイプです。"),
    "IN": ("思慮深い", "あなたは物事を深く考える傾向があります。慎重な判断ができ、洞察力に優れています。"),
    "IS": ("職人肌", "あなたはコツコツと努力を積み重ねる職人タイプです。自分のペースで着実に成果を出します。"),
    "ENTP": ("アイデアマン", "あなたは新しいアイデアを生み出すのが得意なタイプです。柔軟な発想力で周囲を驚かせます。"),
    "INTJ": ("戦略家", "あなたは計画的に物事を進める戦略家タイプです。論理的に考え、目標達成に向けて努力します。"),
    "ESFP": ("エンターテイナー", "あなたは明るく社交的で、人を楽しませるのが得意です。周囲を笑顔にする力を持っています。"),
    "ISTJ": ("管理者", "あなたは責任感が強く、ルールを大切にするタイプです。しっかりと物事を管理し、着実に進めます。"),
    "INFJ": ("理想主義者", "あなたは高い理想を持ち、それに向かって努力するタイプです。人の気持ちを理解し、共感力も高いです。"),
    "ISTP": ("実践派", "あなたは実践的なスキルを持ち、手を動かしながら学ぶのが得意なタイプです。冷静な判断力もあります。"),
    "ENTJ": ("指導者", "あなたはリーダーシップがあり、周囲を引っ張る力を持っています。目標に向かって突き進むタイプです。"),
    "ISFJ": ("献身的", "あなたは周囲に気を配り、思いやりを大切にするタイプです。人のサポートをするのが得意です。"),
    "ENFJ": ("インスピレーションメーカー", "あなたは周囲を鼓舞し、前向きな影響を与えるタイプです。リーダーとして活躍できる素質があります。"),
    "ESTJ": ("リーダー気質", "あなたは現実的でリーダーシップに優れたタイプです。組織をまとめ、しっかりと管理することができます。"),
    "ESTP": ("冒険家", "あなたはスリルを楽しむタイプで、新しいことに挑戦するのが好きです。行動力があり、柔軟に動けます。"),
    "INTP": ("論理的思考家", "あなたは理論的に物事を考えるのが得意です。知識欲が旺盛で、深く掘り下げることを好みます。"),
}

def result_page():
    final_result = st.session_state["final_result"]
    result_name, result_description = result_labels.get(final_result, ("診断結果不明", "該当する診断結果が見つかりませんでした。"))

    st.title("診断結果")
    st.write(f"あなたの診断結果は: **{result_name}**")
    st.write(f"**{result_description}**")

    st.write(f"ここに文言を入れる")

    # アンケートページに遷移するボタンを追加
    st.markdown(
        """
        <div style="text-align: center; margin-top: 30px;">
            <a href="https://docs.google.com/forms/d/e/1FAIpQLSetyoLX4bXlkEGmRhhhDGltfLDCAg52NDThs_S0TWNeo7ienA/viewform" target="_blank">
                <button style="background-color:#4CAF50; color:white; padding:10px 20px; border:none; cursor:pointer;">
                    アンケートに進む
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)

    # 戻るボタンを追加
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px;">
            <a href="https://chilchil2-qxehnzkrhvqchpqqgjsgum.streamlit.app/?page=result#63d94710">
                <button style="background-color:#f44336; color:white; padding:10px 20px; border:none; cursor:pointer;">
                    戻る
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)



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

    if total_score == 0 and answers:
        total_score = score_mapping.get(answers[0], 0)

    if total_score > 0:
        return label1
    elif total_score < 0:
        return label2
    else:
        return label3


# 日本時間のタイムゾーンを指定
japan_timezone = pytz.timezone('Asia/Tokyo')

# 現在の日本時間を取得
now = datetime.now(japan_timezone).strftime("%Y-%m-%d %H:%M:%S")


try:
            sheet.append_row([now, final_result] + responses)
except Exception as e:
            st.error(f"スプレッドシートへの記録に失敗しました: {e}")
            st.stop()

st.session_state["final_result"] = final_result 
st.session_state["result_page"] = True
st.rerun()  

# メイン処理
def main():
    if st.session_state.get("result_page", False):
        result_page()
    else:
        diagnosis_page()

if __name__ == "__main__":
    main()
