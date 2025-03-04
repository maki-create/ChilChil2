import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 活動家A")

st.write("活動家タイプのあなた。とにかく楽しいことやお祭り騒ぎが好きで、イベントやコラボカフェなどお出かけに積極的な活動家さん。交友関係が広く、オタ活を通してできた友達と親友になることもあります。プライベートも充実していて毎日輝いているでしょう。
推しのすべてが好きなので、周りが推しの魅力に気づいてくれることに喜びを感じます。ただ、あまりの熱量に相手が圧倒されてしまうことも。布教に失敗してもへこまないでね
")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
