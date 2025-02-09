import streamlit as st

st.title("診断結果")

# 診断結果を取得
if "result_自己分析" in st.session_state:
    final_result = f"""
    **あなたの診断結果**
    - {st.session_state['result_自己分析']['result_他者との関係']}
    -['result_職業適性']['result_ライフスタイル']
    """
    st.success(final_result)
else:
    st.warning("まだ診断が行われていません。")

# 戻るボタン
if st.button("ホームに戻る"):
    st.switch_page("app.py")
