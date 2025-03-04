import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: フォロワーB")

st.write("フォロワータイプのあなた。普段あまり自己主張をしないフォロワーさんですが、ひっそり推しにエールを送る姿はオタクの鑑とも言えます。short動画やXなどSNSの使い方が上手なので、幅広く様々なジャンルについて把握しているマネージャーさん。「名前は知っているけれど、詳しくは……」という人物に目を向けてみると、深い沼が広がっているかもしれませんよ")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
