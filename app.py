import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

google_credentials = st.secrets["google_credentials"]

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(google_credentials), scope)
client = gspread.authorize(creds)

spreadsheet_id = st.secrets["google_credentials"]["spreadsheet_id"]
sheet = client.open_by_key(spreadsheet_id).sheet1

st.session_state.setdefault("final_result", None)
st.session_state.setdefault("result_page", False)

result_labels = {
    "EN": ("カリスマ", "あなたはカリスマ性があり、周囲の人を引きつける魅力を持っています。"),
    "ES": ("冒険家", "あなたはスリルを楽しむタイプで、新しいことに挑戦するのが好きです。"),
}

def result_page():
    final_result = st.session_state.get("final_result", "不明")
    result_name, result_description = result_labels.get(final_result, ("診断結果不明", "説明がありません。"))

    st.title("診断結果")
    st.markdown(f"""
        <h2 style='text-align: center; font-size: 36px; color: #ff5733;'>
            あなたの診断結果は: {result_name} ({final_result})
        </h2>
    """, unsafe_allow_html=True)
    st.write(f"**{result_description}**")

def diagnosis_page():
    st.title("性格診断アプリ")
    st.write("各質問に対して選択してください。")

    categories = {
        "カテゴリー1": ["(1)会場が遠くても遠征する", "(2)SNSでたくさんの人と交流する"],
    }

    responses = []
    for category, questions in categories.items():
        for idx, q in enumerate(questions):
            st.write(f"**{q}**")
            options = ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない"]
            options.append("どちらでもない")
            response = st.radio("", options, key=f"{category.replace(' ', '_')}_{idx}", horizontal=True)
            responses.append(response)

    if st.button("診断を実行"):
        if len(responses) < len(categories) * 2:
            st.error("全ての質問に回答してください")
            st.stop()

        final_result = "EN"  # 仮のロジック

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            sheet.append_row([now, final_result] + responses)
        except Exception as e:
            st.error(f"スプレッドシートへの記録に失敗しました: {e}")
            st.stop()

        st.session_state["final_result"] = final_result
        st.session_state["result_page"] = True
        st.rerun()

def main():
    if st.session_state.get("result_page", False) is True:
        result_page()
    else:
        diagnosis_page()

if __name__ == "__main__":
    main()
