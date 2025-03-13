import streamlit as st

if "responses" in st.session_state:
    st.title("自由記述アンケート")
    st.write("以下の質問に自由に回答してください。")
    
    free_responses = []
    questions = [
        "あなたが一番好きな推し活のエピソードを教えてください。",
        "推し活をしていて嬉しかったことは何ですか？",
        "推し活をしていて大変だったことは何ですか？"
    ]
    
    for i, question in enumerate(questions):
        response = st.text_area(f"{i+1}. {question}", key=f"free_response_{i}")
        free_responses.append(response)
    
    if st.button("診断を実行"):
        # 診断結果の計算などの処理
        final_result = "診断結果"
        st.success(f"診断結果: {final_result}")
