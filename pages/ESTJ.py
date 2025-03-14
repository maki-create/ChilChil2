import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 旅人A ")

st.write("旅人タイプのあなた。推し活を通したコミュニケーションが好きで、色んなジャンルにたくさんの推しがいる旅人さん。フットワークは軽いけれどお財布の紐が固く、キャパオーバーにはならないようにする冷静さも持ち合わせています。オタク友達が多いあなたは、その界隈のプロフェッショナルから布教を受けることも多いはず。周りに影響を受けて染まりやすいので、推しと沼が増え過ぎないように気を付けて。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
