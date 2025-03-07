import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 啓蒙者A")

st.write("啓蒙者タイプのあなた。推しに対してきちんと自分の考えを持つあなたは、悩めるオタクを導くオピニオンリーダーのような輝きを放っています。SNSで推しの情報や推し作家さんの作品をいいねするスピードはもはや流星です。とにかく推しのために行動するので、数か月前に買ったグッズが届く頃にはもう何を買ったか覚えていない……なんていうこともしばしば。流通センターのような手さばきでグッズ収集をするプロです。芯が強いのがあなたの魅力ですが、時として周りと対立してしまうことも。自分を貫くのも大切ですが、少し視野を広く持つことも大切です
")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
