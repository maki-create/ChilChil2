import streamlit as st

# CSSでラジオボタンの配置を調整
st.markdown("""
    <style>
    div[data-testid="stRadio"] > label {
        display: flex;
        flex-direction: row;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# スコア計算関数（スコアルール変更）
def calculate_result(answers, label1, label2):
    score_mapping = {
        "当てはまる": 2,
        "当てはまらない": -2,
        "どちらでもない": 1,
        "意味が分からない": 0
    }
    
    total_score = sum(score_mapping[ans] for ans in answers)

    if total_score > 0:
        return label1
    elif total_score < 0:
        return label2
    else:
        return label1  # カンマを避けるため、同点の場合は label1 を優先

# Streamlit UI
st.title("性格診断アプリ")
st.write("各質問に対して「当てはまる」「当てはまらない」「どちらでもない」「意味が分からない」の中から選んでください。")

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
        col1, col2 = st.columns([2, 3])  # 質問とラジオボタンを横並びにする
        with col1:
            st.write(f"**{q}**")  # 質問を左に配置
        with col2:
            response = st.radio("", ["当てはまる", "当てはまらない", "どちらでもない", "意味が分からない"], key=f"{category}_{q}", horizontal=True)  # 4択に変更
            responses.append(response)

if st.button("診断を実行"):
    result_I_E = calculate_result(responses[0:3], "I", "E")
    result_S_N = calculate_result(responses[3:6], "S", "N")
    result_T_F = calculate_result(responses[6:9], "T", "F")
    result_J_P = calculate_result(responses[9:12], "J", "P")

    final_result = f"{result_I_E}{result_S_N}{result_T_F}{result_J_P}"
    st.session_state["final_result"] = final_result

    # 診断結果のページに遷移（カンマが入らないよう修正済み）
    st.switch_page(f"pages/{final_result}.py")

