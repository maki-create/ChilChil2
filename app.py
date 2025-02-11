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
creds_dict = st.secrets["google_credentials"]

# Google Sheets API認証を設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Googleスプレッドシートを開く（シートのURLまたはIDを指定）
spreadsheet_id = "1eKhD929QC8fdvse2G92woknfWh7Dnv7Pmi2w1ZqXWCM"  # ★スプレッドシートのIDを入れる
sheet = client.open_by_key(spreadsheet_id).sheet1  # 1枚目のシートを選択

# CSSでラジオボタンの配置を調整
st.markdown("""
    <style>
    div[data-testid="stRadio"] > label {
        display: flex;
        flex-direction: row;
        gap: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# スコア計算関数（スコアルール変更）
def calculate_result(answers, label1, label2,label3):
    score_mapping = {
        "当てはまる": 2,
        "当てはまらない": -3,
        "どちらでもない": 1,
        "意味が分からない": 0
    }
    
    total_score = sum(score_mapping[ans] for ans in answers)

    if total_score > 0:
        return label1
    elif total_score < 0:
        return label2
    else:
        return label3 # カンマを避けるため、同点の場合は label1 を優先

# Streamlit UI
st.title("性格診断アプリ")
st.write("各質問に対して「当てはまる」「当てはまらない」「どちらでもない」「意味が分からない」の中から選んでください。")

# 質問
categories = {
     "IかEか": [
                "質問1", 
                "質問2", 
                "質問3",
                "質問4",
                "質問5",
                "質問6",
                "質問7",
                "質問8",
                "質問9"],
     "カテゴリー2": ["質問10",
                "質問11",
                "質問12",
                "質問13",
                "質問14"
                ,"質問15"
                ,"質問16"
                 ,"質問17"
                ,"質問18"],
     "カテゴリー3": ["質問19",
                "質問20",
                "質問21",
                "質問22",
                "質問23",
                "質問24",
                "質問25",
                "質問26",
                "質問27"],
     "カテゴリー4": ["質問28",
                "質問29",
                "質問30",
                "質問31",
                "質問32",
                "質問33",
                "質問34"
                ,"質問35",
                "質問36",]
                
}

responses = []  # 初期化を追加

for category, questions in categories.items():
    for idx, q in enumerate(questions):
        col1, col2 = st.columns([2, 2])  # 質問とラジオボタンを横並びにする
        with col1:
            st.write(f"**{q}**")  # 質問を左に配置
        with col2:
            response = st.radio("", ["当てはまる", "当てはまらない", "どちらでもない", "意味が分からない"], 
                                key=f"{category}_{idx}", horizontal=True)  
            responses.append(response)

        # 質問と質問の間に改行を入れる
        st.markdown("<br>", unsafe_allow_html=True)  


if st.button("診断を実行"):
    result_I_E = calculate_result(responses[0:9], "I", "E", "意味が分からないばかり答えています)")
    result_S_N = calculate_result(responses[10:18], "S", "N", "意味が分からないばかり答えています)")
    result_T_F = calculate_result(responses[19:27], "T", "F", "意味が分からないばかり答えています)")
    result_J_P = calculate_result(responses[28:36], "J", "P", "意味が分からないばかり答えています)")

    final_result = f"{result_I_E}{result_S_N}{result_T_F}{result_J_P}"
    st.session_state["final_result"] = final_result

    # 現在の日時を取得
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 解答内容を一緒に記録する
    try:
        # ユーザーの解答と診断結果をスプレッドシートに記録
        sheet.append_row([now, result_I_E_意味が分からないばかり答えています, result_S_N_意味が分からないばかり答えています, result_T_F_意味が分からないばかり答えています, result_J_P_意味が分からないばかり答えています, final_result] + responses)
        
    except Exception as e:
        st.error(f"スプレッドシートへの記録に失敗しました: {e}")

# 診断結果のページに遷移
    st.switch_page(f"pages/{final_result}.py")
