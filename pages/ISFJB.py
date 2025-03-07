import streamlit as st

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)


st.title("診断結果: マネージャーB")

st.write("
マネージャータイプのあなた。推しにズブズブに沼ってお金も時間も使いすぎることはないため、推し疲れに陥らず長く細くオタクを続けられているかもしれませんね。推しができると誰かに良さを伝えたいという気持ちからSNSや身内に急に布教し始めることもあるのではないでしょうか。好きが乗じて動画編集を始めて布教をしてくれるタイプも中にはいそうなので誰かの沼の入口に！いつも穏やかに推し活ができているマネージャーさんですが、大炎上やSNSで巻き起こる討論では落ち込んでしまうことも…。マネージャーさんが辛くなってしまうことからは距離を取って自分のペースで推し活を維持しよう。")

# 「元のアプリに戻る」ボタン
if st.button("元のページに戻る"):
    st.switch_page("app.py")  
