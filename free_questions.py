import streamlit as st

st.title("自由記述の質問")

q1 = st.text_area("あなたが一番影響を受けた作品は何ですか？")
q2 = st.text_area("推しのどんなところが好きですか？")
q3 = st.text_area("推し活の中で最も印象に残っているエピソードを教えてください。")

if st.button("診断結果を表示"):
    st.switch_page("result")

