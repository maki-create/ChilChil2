import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 語り部A ")

st.write(" 語り部タイプのあなた。お金も時間も惜しまないオタクのあなたは、一日が30時間あったらいいのに……と考えてしまうこともあると思います。布教や創作活動も好きなので、何かのタスクや締め切りに追われていることも多いはず。推しのことなら何時間でも喋れるので、周りから推しの博士だと思われているかも。たくさんの界隈に推しがいるので、常に金欠になりがち。時には口座残高と向き合うことも大切です")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
