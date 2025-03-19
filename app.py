import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

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

# 診断結果を人間向けのラベルに変換する辞書
result_labels = {
    "EN": "カリスマ",
    "ES": "エネルギッシュ",
    "IN": "思慮深い",
    "IS": "職人肌",
    "ENTP": "アイデアマン",
    "INTJ": "戦略家",
    "ESFP": "エンターテイナー",
    "ISTJ": "管理者",
    "INFJ": "理想主義者",
    "ISTP": "実践派",
    "ENTJ": "指導者",
    "ISFJ": "献身的",
    "ENFJ": "インスピレーションメーカー",
    "ESTJ": "リーダー気質",
    "ESTP": "冒険家",
    "INTP": "論理的思考家"
}

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

# 結果ページの表示
def result_page():
    final_result = st.session_state["final_result"]
    translated_result = result_labels.get(final_result, "診断結果不明")

    st.title("診断結果")
    st.write(f"あなたの診断結果は: **{translated_result}** ({final_result})")

# 診断ページ
def diagnosis_page():
    st.title("性格診断アプリ")
    st.write("各質問に対して「当てはまる」「当てはまらない」「どちらでもない」「やや当てはまる」「あまり当てはまらない」の中から選んでください。")

    categories = {
        "カテゴリー1": ["(1)会場が遠くても積極的に遠征しに行く", "(2)SNSでたくさんの人と交流するのが楽しい"],
        "カテゴリー2": ["(10)推しの絶対的な味方でいたい", "(11)推しは近い存在でいてほしい"]
    }
    
    responses = []
    for category, questions in categories.items():
        for idx, q in enumerate(questions):
            st.write(f"**{q}**")
            options = ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない"]
            if idx not in [0, 9, 18, 27, 36]:  
                options.append("どちらでもない")
            response = st.radio("", options, key=f"{category}_{idx}", horizontal=True)
            responses.append(response)

    # 診断ボタン
    if st.button("診断を実行"):
        if len(responses) < 4:  # 例では質問が4つなので調整
            st.error("全ての質問に回答してください")
            st.stop()

        final_result = (
            f"{calculate_result(responses[0:2], 'E', 'I', '意味が分からない')}"
            f"{calculate_result(responses[2:4], 'N', 'S', '意味が分からない')}"
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            sheet.append_row([now, final_result] + responses)
        except Exception as e:
            st.error(f"スプレッドシートへの記録に失敗しました: {e}")
            st.stop()

        st.session_state["final_result"] = final_result
        st.session_state["result_page"] = True
        st.rerun()  # 🔄 修正ポイント

# メイン処理
def main():
    if st.session_state.get("result_page", False):
        result_page()
    else:
        diagnosis_page()

if __name__ == "__main__":
    main()
