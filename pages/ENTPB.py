import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 啓蒙者B")

st.write("啓蒙者タイプのあなた。推しに対してきちんと自分の考えを持つあなたは、悩めるオタクを導くオピニオンリーダーのような輝きを放っています。SNSが得意で、推しの情報収集や発信はお手のものです。
とにかく現場が大好きで、数か月前に入金を済ませたライブは当日実質無料に感じてしまうお茶目な一面も。
芯が強いのがあなたの魅力ですが、時として周りと対立してしまうことも。自分を貫くのも大切ですが、少し視野を広く持つことも大切です
")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
