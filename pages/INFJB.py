import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 保護者B")

st.write("保護者タイプのあなた。推しのことが大好きでSNSを使った布教活動に勤しむ日々ですが、保護者さん自身でどこまで沼るのかのボーダーを引けるので時間やお金を使いすぎて後悔…なんてことは少ないでしょう。推しとの良い距離感を保てるので心の負担も少ない楽しいオタクライフを送れそう。推しが増えすぎてしまうと今の距離感を保つことが難しくなることもありそうなので色んな沼に浸かりすぎないマイペースでいきましょう。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
