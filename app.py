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

# 診断結果を人間向けのラベルと説明文に変換する辞書
result_labels = {
    "ENFP": ("自由な精神", "あなたは好奇心旺盛で、新しいことに挑戦するのが好きです。https://docs.google.com/forms/d/e/1FAIpQLSetyoLX4bXlkEGmRhhhDGltfLDCAg52NDThs_S0TWNeo7ienA/viewform"),
    "ENTP": ("アイデアマン", "あなたは新しいアイデアを生み出すのが得意なタイプです。"),
    "INTJ": ("戦略家", "あなたは計画的に物事を進める戦略家タイプです。"),
    "INFJ": ("助言者", "あなたは高い理想を持ち、それに向かって努力するタイプです。"),
    "ESTP": ("冒険家", "あなたはスリルを楽しむタイプで、新しいことに挑戦するのが好きです。"),
    "ESFP": ("エンターテイナー", "あなたは明るく社交的で、人を楽しませるのが得意です。"),
    "ISTJ": ("管理者", "あなたは責任感が強く、ルールを大切にするタイプです。"),
    "ISFJ": ("献身的", "あなたは周囲に気を配り、思いやりを大切にするタイプです。"),
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

# 診断結果ページ
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

# 診断ページ
def diagnosis_page():
    st.title("性格診断アプリ")
    st.write("各質問に対して選択してください。")

    categories = {
        "外向(E) - 内向(I)": ["(1)会場が遠くても遠征する", "(2)SNSでたくさんの人と交流する"],
        "直感(N) - 感覚(S)": ["(3)イベントごとが好き", "(4)推しの投稿にコメントをする"],
        "感情(F) - 思考(T)": ["(5)推しの幸せを第一に考える", "(6)推しの成功を自分のことのように喜ぶ"],
        "柔軟(P) - 計画(J)": ["(7)予定が変わっても柔軟に対応する", "(8)スケジュールをきっちり決める"],
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

        # 各軸のスコアを計算
        e_or_i = calculate_result(responses[0:2], "E", "I", "不明")
        n_or_s = calculate_result(responses[2:4], "N", "S", "不明")
        f_or_t = calculate_result(responses[4:6], "F", "T", "不明")
        p_or_j = calculate_result(responses[6:8], "P", "J", "不明")

        # MBTI タイプを決定
        final_result = f"{e_or_i}{n_or_s}{f_or_t}{p_or_j}"

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    if st.session_state.get("result_page", False) is True:
        result_page()
    else:
        diagnosis_page()

if __name__ == "__main__":
    main()
