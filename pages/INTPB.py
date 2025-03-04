import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 思想家B")

st.write("思想家タイプのあなた。推しの出演作やMVなどを持ち前の考察力を活かした楽しみ方ができているのではないでしょうか。SNSや周りの人にそれを積極的に話すことは少ないですが、オタク友達と話すときにその考察を全開にして話して盛り上がることも多そう。思慮深い思想家さんではありますが、推しの炎上などで考えすぎて落ち込んでしまうことがありそう。そんな時はSNSと距離を取ってみるといい息抜きができそう。
")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
