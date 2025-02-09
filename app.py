import streamlit as st

# CSSでラジオボタンを横並びにする
st.markdown("""
    <style>
    div[data-testid="stRadio"] > div {
        display: flex;
        justify-content: space-evenly;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True
with st.sidebar:
    st.empty()  # 何も表示しない
)

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
    "自己分析": ["質問 1", "質問 2", "質問 3"],
    "他者との関係": ["質問 4", "質問 5", "質問 6"],
    "職業適性": ["質問 7", "質問 8", "質問 9"],
    "ライフスタイル": ["質問 10", "質問 11", "質問 12"]
}

responses = []

for category, questions in categories.items():
    st.subheader(f"{category}")
    for q in questions:
        response = st.radio(f"**{q}**", ["〇", "×"], key=f"{category}_{q}")
        responses.append(response)

if st.button("診断を実行"):
    result_I_E = calculate_result(responses[0:3], "I", "E")
    result_S_N = calculate_result(responses[3:6], "S", "N")
    result_T_F = calculate_result(responses[6:9], "T", "F")
    result_J_P = calculate_result(responses[9:12], "J", "P")

    final_result = f"{result_I_E}{result_S_N}{result_T_F}{result_J_P}"
    st.session_state["final_result"] = final_result

    # 診断結果のページに遷移
    st.switch_page(f"pages/{final_result}.py")
