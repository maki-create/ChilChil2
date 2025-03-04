import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: ユートピアンA")

st.write("ユートピアンタイプのあなた。SNS等を使って布教することも楽しめるユートピアンさんは新規さんの分からないことがあったら的確に優しく答えてくれるので周りからは優しいオタクだと思われていそう。新規ホイホイ的な役割を担ってくれるので界隈の布教にも一役を担っていることでしょう。「推しのためならなんでもできる！」を体現していて一度創作活動を始めると時間を忘れて没頭し、推し関連のグッズは何が何でも集めたい派ですね。時間とお金の使い方を一度立ち止まって考えてみる事が長くオタクを続けられるコツです")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
