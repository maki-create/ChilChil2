import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 愛好家B")

st.write("好家タイプのあなた。推しが売れてほしいという想いを持ちつつも実際売れると複雑な心境を持っている悩めるオタク。それでも売れてほしい気持ちは強いので布教活動も積極的。愛情表現として推しコラボのグッズや公式グッズの購入も惜しまず、推しのSNS更新には真っ先に反応してくれます。推し活に全力な愛好家さんはその分推し活で悩むことも多いかも。意見の合う友達と情報交換ができると負担が少なくなりそう。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
