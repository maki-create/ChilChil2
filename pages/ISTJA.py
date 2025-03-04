import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果:フォロワーA ")

st.write("フォロワータイプのあなた。普段あまり自己主張をしないフォロワーさんですが、推しを優しく見守り、影ながら応援する包容力の持ち主です。short動画やXなどSNSの使い方が上手なので、幅広く様々なジャンルについて把握していると思います。一方で「Xで流れてくるファンアートは見るけれど本編は知らない……」なんてことも？ 勇気を出して新しいジャンルに飛び込めば、深い沼が見つかるかもしれませんよ。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
