import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

st.title("診断結果: ESTJ")

st.write("あなたは戦略的な思考を持ち、長期的な視野で物事を計画するタイプです。")

# ホームに戻るボタン
if st.button("ホームに戻る"):
    st.switch_page("app.py")  # `app.py` に戻る
