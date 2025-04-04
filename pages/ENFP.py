import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: カリスマA")

st.write("カリスマタイプのあなた。日常のすべてを推しに向けて、できる限り時間を使う姿は周りから尊敬の眼差しを向けられています。推しがビッグになるためならSNSや身内への布教も積極的に行っています。オタク友達も多くSNSでの布教も上手。カリスマならではの余裕を周囲の人は感じていそうですね。推しを活力に日々仕事も勉強をがんばる愛の人です。ただ、ストッパーが機能しないのでつい勢いで突っ走ってしまうことも？ 自分のブレーキをたまには点検してね")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
