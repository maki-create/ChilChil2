import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 演出家A")

st.write("演出家タイプのあなた。お財布と時間に余裕があればライブやイベントに顔を出したり、ぬい活をしたりとフットワークが軽めのオタクです。自分の人生を彩るオタ活をするあなたは輝いています。推しの雰囲気に寄せたコーディネートをしたり、概念ソングを見つけたりすることがとても上手です。寝る前や1人のときに妄想が止まらないことも。推しの存在はとても尊いですが、寝不足には気を付けて
")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
