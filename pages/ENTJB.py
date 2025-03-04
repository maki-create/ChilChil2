import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 演出家B")

st.write("演出家タイプのあなた。お財布と時間に余裕があればライブやイベントに顔を出したり、ぬい活をしたりとフットワークが軽めのオタクです。自分の人生を彩るオタ活をするあなたは輝いています。流行りに敏感で、最新トレンドを押さえているおしゃれさんでもあります。推しが大好きであるがゆえに、推しになにかがあるとダメージを受けがち。1人で枕を濡らさず周りに相談してみましょう")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
