import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 保護者A ")

st.write("保護者タイプのあなた。推しのことが大好きな気持ちが溢れて布教活動を行う方も多そうですね。保護者さん自身でどこまで沼るのかのボーダーを引けるので時間やお金を使いすぎて後悔…なんてことは少ないでしょう。深入りしすぎないからこそ推しがいっぱいいる方もいそうですね。推しとの良い距離感を保てているので心の負担も少ない楽しいオタクライフを送れそう。オタクとして価値観が合わないとオタクとしてのあり方で負担になってしまうことがあるかも…。自分の居心地の良い場所を見つけてこれからも良いオタク人生を。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
