import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 研究者B")

st.write("研究者タイプのあなた。推しのことを深く知りたいと思う研究者のような知識欲と想像力を持ち合わせています。様々な媒体を使って推しの考え方や身に着けているものを追求しがち。もしかしたら推しの身に着けているアクセサリーなどにも詳しいかもしれません。周りの人からは「研究者さんに聞けば分かる！」と思われていることもありそうです。推しへの知識が深い研究者さんは、情報収集に抜け目のない生き字引ですが自分よりも熱量が浅い人に対して厳しくなってしまうかも…。自分にも他人にも厳しくしすぎないことが安定したオタク活動になりそう。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
