import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 理想主義者B")

st.write("理想主義者タイプのあなた。推しへの愛情と自分の生活のバランスがよくとれている理想主義者さんは寝る前にファンが投稿したSNSや公式から供給されたコンテンツを見ることが一日の楽しみ。何気なく見たyoutubeのライブ映像から別の沼にハマって抜けられない…なんてことも多そう。熱しやすく冷めにくいタイプのため沼が増えると時間のバランスが崩壊してしまうかも。時間の使い方には気を付けてみましょう")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
