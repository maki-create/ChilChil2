import streamlit as st

# CSSでラジオボタンのラベルを横並びにする
st.markdown("""
    <style>
    div[data-testid="stRadio"] label {
        display: inline-flex;
        margin-right: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
""", unsafe_allow_html=True)

# スコア計算関数
def calculate_result(answers, label1, label2):
    score1 = sum(1 for ans in answers if ans == '〇')
    score2 = sum(1 for ans in answers if ans == '×')

    if score1 > score2:
        return label1
    elif score2 > score1:
        return label2
    else:
        return f"{label1}, {label2}"

# Streamlit UI
st.title("性格診断アプリ")
st.write("各質問に対して「〇」または「×」を選んでください。")

# 質問データ
categories = {
    "コンテンツ1": ["質問 1", "質問 2", "質問 3"],
    "コンテンツ2": ["質問 4", "質問 5", "質問 6"],
    "コンテンツ3": ["質問 7", "質問 8", "質問 9"],
    "コンテンツ4": ["質問 10", "質問 11", "質問 12"]
}

responses = []

for category, questions in categories.items():
    st.subheader(f"{category}")
    for q in questions:
        col1, col2, col3 = st.columns([3, 1, 1])  # 質問、〇、×の3列を作成

        with col1:
            st.write(f"**{q}**")  # 質問を左側に表示
        with col2:
            if st.radio(f"{q}_〇", ["〇", "×"], index=0, key=f"{category}_{q}") == "〇":
                responses.append("〇")
            else:
                responses.append("×")

if st.button("診断を実行"):
    result_I_E = calculate_result(responses[0:3], "I", "E")
    result_S_N = calculate_result(responses[3:6], "S", "N")
    result_T_F = calculate_result(responses[6:9], "T", "F")
    result_J_P = calculate_result(responses[9:12], "J", "P")

    final_result = f"{result_I_E}{result_S_N}{result_T_F}{result_J_P}"
    st.session_state["final_result"] = final_result

    st.write(f"診断結果: **{final_result}**")

