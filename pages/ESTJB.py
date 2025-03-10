import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 旅人B")

st.write("旅人タイプのあなた。推し活を通したコミュニケーションが好きで、色んなジャンルにたくさんの推しがいる旅人さん。推し活でダメージを受けることもありますが、そのたびに別の界隈の推しを見て心を癒すことができます。フットワークは軽いけれどキャパオーバーにはならないようにする冷静さも持ち合わせています。様々な現場と遠征が好きで、地方の美味しいお店にも詳しい頼れる存在。一方で、熱しやすく冷めやすい傾向があるので、熱量が長続きしないことも。推し活ペースを無理して友達に合わせないように気を付けて。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
