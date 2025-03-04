import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: マネージャーB")

st.write("マネージャータイプのあなた。推しのことが大好きではあるが、深入りしすぎることが少ないので長く細くオタクができている。少しの炎上や熱愛でも動揺することなく生活の楽しみの一部として推しのSNSやコンテンツを素直に楽しめているでしょう。推しの存在が生活の中で中心になりすぎないので他の趣味や生活にも同じくらい重心を置くことができそう。いつも穏やかなマネージャーさんですが、大炎上やSNSでの討論で落ち込んでしまうこともありそう。SNSやマネージャーさんが辛くなってしまうことからは距離を取って自分のペースで推し活を維持しよう")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
