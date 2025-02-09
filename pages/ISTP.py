import streamlit as st

st.title("診断結果: ISTP")

st.write("あなたは戦略的な思考を持ち、長期的な視野で物事を計画するタイプです。")

# ホームに戻るボタン
if st.button("ホームに戻る"):
    st.switch_page("Home")  # `app.py` に戻る
