import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 支援者Ａ ")

st.write("支援者タイプのあなた。SNSでもリアルでも積極的に布教活動を行う宣教師型オタクのあなた。交友関係も広く、オタク友達とイベントに参加することも多いはず。ハマる一歩手前のオタクを持ち前の優しさと布教力で沼に沈めることができます。推しの供給に爆発して自分が創作を始めてしまうこともあるあるです。ただ、熱しやすく冷めやすい一面もあるので、時には立ち止まって考えることも大切です")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
