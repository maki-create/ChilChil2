import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Streamlit Secretsから情報を取得
google_credentials = st.secrets["google_credentials"]

# Google API 認証
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(dict(google_credentials), scope)
client = gspread.authorize(creds)

# Googleスプレッドシートを開く
spreadsheet_id = st.secrets["google_credentials"]["spreadsheet_id"]
sheet = client.open_by_key(spreadsheet_id).sheet1  # 1枚目のシートを選択

# セッションステートの初期化（エラー回避）
st.session_state.setdefault("final_result", None)
st.session_state.setdefault("result_page", False)


# 診断結果の対応表
result_mapping = {
    "ENFP": "カリスマ",
    "ES": "冒険家",
    "IN": "思索家",
    "IS": "職人",
    "ENTP": "発明家",
    "ENTJ": "指揮官",
    "INTP": "哲学者",
    "INTJ": "戦略家",
    "ENFP": "自由な精神",
    "INFJ": "助言者",
    "ESFP": "エンターテイナー",
    "ISFP": "芸術家",
    "ESTP": "挑戦者",
    "ISTP": "職人気質",
    "ESTJ": "管理者",
    "ISTJ": "実務家"
}

# 診断結果に対応する説明文
result_descriptions = {
    "カリスマ": "あなたはカリスマ性があり、周囲の人を引きつける魅力を持っています。https://docs.google.com/forms/d/e/1FAIpQLSetyoLX4bXlkEGmRhhhDGltfLDCAg52NDThs_S0TWNeo7ienA/viewform",
    "冒険家": "あなたは好奇心旺盛で、新しいことに挑戦するのが大好きです。",
    "思索家": "深く物事を考え、理論的に問題を解決するのが得意です。",
    "職人": "実践的なスキルに優れ、細かい作業が得意です。",
    # 他のタイプも追加可能
}

# スコア計算関数
def calculate_result(answers, label1, label2, label3):
    score_mapping = {
        "当てはまる": 2,
        "やや当てはまる": 1,
        "どちらでもない": 0,
        "あまり当てはまらない": -1,
        "当てはまらない": -2,
    }
    
    total_score = sum(score_mapping[ans] for ans in answers)

    # 合計値が0の場合、最初の質問の結果を参照
    if total_score == 0 and answers:
        total_score = score_mapping.get(answers[0], 0)

    if total_score > 0:
        return label1
    elif total_score < 0:
        return label2
    else:
        return label3

# 結果ページの表示
def result_page():
    final_result = st.session_state["final_result"]
    translated_result = result_labels.get(final_result, "診断結果不明")

    st.title("診断結果")

    result_name = result_mapping.get(final_result, "不明")  # 対応がない場合は「不明」に
    result_description = result_descriptions.get(result_name, "診断結果の説明が見つかりません。")

    # 診断結果の表示
    st.markdown(f"""
        <h2 style='text-align: center; font-size: 36px; color: #ff5733;'>
             {result_name} 
        </h2>
        """, unsafe_allow_html=True)

    # 診断結果の説明を表示
    st.write(f"**{result_description}**")
    
    # 戻るボタンの追加
    if st.button("元のページに戻る"):
        st.session_state["result_page"] = False
        st.experimental_rerun()  # ページをリセットして診断ページに戻る

# 診断ページ
def diagnosis_page():
    st.title("性格診断アプリ")
    st.write("各質問に対して「当てはまる」「当てはまらない」「どちらでもない」「やや当てはまる」「あまり当てはまらない」の中から選んでください。")

    categories = {
        "カテゴリー1": ["(1)会場が遠くても積極的に遠征しに行く", "(2)SNSでたくさんの人と交流するのが楽しい"],
        "カテゴリー2": ["(10)推しの絶対的な味方でいたい", "(11)推しは近い存在でいてほしい"],
        "カテゴリー3": ["(19)推しの絶対的な味方でいたい", "(20)推しは近い存在でいてほしい"],
        "カテゴリー4": ["(28)推しの絶対的な味方でいたい", "(11)推しは近い存在でいてほしい"],
    }
    
    responses = []
    for category, questions in categories.items():
        for idx, q in enumerate(questions):
            st.write(f"**{q}**")
            options = ["当てはまる", "やや当てはまる", "あまり当てはまらない", "当てはまらない"]
            if idx not in [0, 9, 18, 27, 36]:  
                options.append("どちらでもない")
            response = st.radio("", options, key=f"{category}_{idx}", horizontal=True)
            responses.append(response)

    # 診断ボタン
    if st.button("診断を実行"):
        if len(responses) < 4:  # 例では質問が4つなので調整
            st.error("全ての質問に回答してください")
            st.stop()

        final_result = (
            f"{calculate_result(responses[0:2], 'E', 'I', '意味が分からない')}"
            f"{calculate_result(responses[2:4], 'N', 'S', '意味が分からない')}"
        )

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            sheet.append_row([now, final_result] + responses)
        except Exception as e:
            st.error(f"スプレッドシートへの記録に失敗しました: {e}")
            st.stop()

        st.session_state["final_result"] = final_result
        st.session_state["result_page"] = True
        st.rerun()  # 🔄 修正ポイント

# メイン処理
def main():
    if st.session_state.get("result_page", False):
        result_page()
    else:
        diagnosis_page()

if __name__ == "__main__":
    main()
