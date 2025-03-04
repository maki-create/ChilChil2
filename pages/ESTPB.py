import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 株主B")

st.write(" 株主タイプのあなた。遠征やグッズ収集などすべて抜かりないあなたはまさにプロのオタク。ガチガチに構築されたネットワークによって情報を漏らさず集めている姿は諜報部員に見えることも。自分の理想の推しに出会ったとき、時間もお金も惜しまず応援する株主さんは、周りにとって頼りがいがある存在です。
推しが炎上してしまったときは周りと意見交換をしたくなるタイプ。ただ、状況によっては傷が深くなることもあるので、1人で考える時間も大切でしょう。
")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
