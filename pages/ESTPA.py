import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: 株主A")

st.write("株主タイプのあなた。ライブやグッズ交換などすべて抜かりないあなたはまさにプロのオタク。長年培った分析力によって鋭い意見を投じるのを得意としています。ファンアートや推しに関する動画を見ているうちにいつの間にか深夜になっている……なんていうことも日常茶飯事。しかし推しが好きであるが故に他のオタクと意見がぶつかってしまうことも。そんなときはそっとSNSから離れてみるのも1つの手！ 心の健康を大切にしてください。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
