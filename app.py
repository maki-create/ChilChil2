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

# TOMLの設定情報を辞書として利用
creds_dict = {
     "type": "service_account",
  "project_id": "aerial-antonym-444302-f9",
  "private_key_id": "e2c40c313a5d840a2cfe97fe2d65c33abd2f975d",
  "private_key": """-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCorQ4EWMLSLWID\nXUtFGr6QdEErmr1Hk8P189Ym9i9O0lXjaxMnzbnIbsJHi7Ds+CM6zR4giu1yHrl0\n1a0ceyx6duL/I5NbFXoWSgTVbsS9Kx3wx1losT29EBvSsK+GQ7qIHn7AQBD4Ldyx\n17rAWUr9qpCh3WcU2RKQTTRvAZQcHuSo0gGB0bgGJnQlIITT60ffstK4QYXdj+5Y\nTX1pN9f7f8ZzguDjElWkbA+hS6M/rjCnnkX27hNEQG/4wv1NO9eNnCNHfnkotVm1\nWWaFT9Mzg29W744B+jjAFnpyu+mAntvZzmCyGvWu5vIq6iqAk9dI9AZd/p1ZvOOv\nvSB+6fO5AgMBAAECggEAEvWkwjNR7rsALd2iNMnNSsJugt65UN7Yo4A9fZKlfagh\n1Fa4R/yVWeStPMqEYBaCKz1cGg9TokS21t2fwDhOJxPO7xvKF+5hkzjNs0nonlTG\n4EYgFCb8CBDT98o5aI+bW2qGF8j7v1G0YV8c1DsVNU8jQ7Z1vD+sGQE8mA+m3MQj\nSS/ZWGS8XZ32lb+/GA34Jp7FVXRzSvMRW1AnILKRVVzr9fAZFegWCyWsJt+dtm1c\nHpIVBjZGfUwqlNFJKnxPoPoi5QKLrkAQBDJteq8m3/wnCH93ssXjFHfOTLadJO9J\nMaAs5ycUQRVfCZx3KQbyHh04/1g5lMPp2s4imlViQQKBgQDjw/eGA/wKXx6/Vah2\nlEM6aWokRE8p+UmKBhqhKfToXC/nVlIYJs7U0dh4t48OkDySzqr97wJ4TPxiq4VO\nD2yyIaXk0Luqa66S3uiz2VtInPBAof0WZoiG4I+3YpU8sjehvlBOia3AJUpGG8U4\np20uW8aZpCZfJegSMtLo7MfZkQKBgQC9lejnP7IH/sRraDEvQKUKFocY9a7hJsKe\njVQnnKIRfY8b2Q6xEbZyaOfjI8fJCZ9dqcANwlYqQ0wwKJCe3SXC6EuHmB/4iN9t\no0mPp77mVBfzlq2d6a9ic+Llujre7yjKavUPfO0vsY4SdM+aGZPPhDKL9zEE8vMe\nKROF3jSjqQKBgCL2VeyQeAPvjfy43V82awtwWwauJai/x3YUccoDcsCoRgIw0fE7\nI8yvWZdONft6UJIIf17zbWGiD6vlwFS3MWw2lgyFrgj+9pE8/mN9HfILhSWmt/7U\nRmjN18HCtD3Y7Yk6eYFUyQMRtlEEukV0DeJr3BSBihJY80K34oA2uIbBAoGAKJm5\nFgTzCHlL8UCP//GVJpLqfbLnr7oQRco4cn89ygccpbcXSV5ktx22Q1N/TpNr+LAI\nvCmZMFXXNB0L06nCk3oR6sjuV9hgGOe2MjiXTlZGBtmG9uF7uNbeiZoXT3TiRG8h\nah6z4Nnidhtj9jlyCSfjd0wJyGiLHjNnxexvU3kCgYAjT48sVk7z7h5pycwTBzOH\nDO4UOT5OcGWj0IURbpDjd8qkf8CbiK7ChG0QLAtOMAsI4lkfu58gsahrf7bNSQjy\nldb2BlCyZ+sHu7sAxWPk8DRsU4Alc3H+GQWgklnnjJZPwAapy1RIjyuoCNmKhAxm\nHpWgPSvIpZuvizu1ncSzew==\n-----END PRIVATE KEY-----\n""",
  "client_email": "service-account@aerial-antonym-444302-f9.iam.gserviceaccount.com",
  "client_id": "100259023955694299607",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40aerial-antonym-444302-f9.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


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
def calculate_result(answers, label1, label2):
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
        return label1  # カンマを避けるため、同点の場合は label1 を優先

# Streamlit UI
st.title("性格診断アプリ")
st.write("各質問に対して「当てはまる」「当てはまらない」「どちらでもない」「意味が分からない」の中から選んでください。")

# 質問データ
categories = {
     "カテゴリー1": ["気になるコンテンツがあっても、ブクマなどしないでまた時間が経てば流れてくるのを待つ", 
                "今のアニメより2010年代に流行ったアニメが好きだ", 
                "他人による作品やキャラクターの解釈を知るために、掲示板等を利用したりする",
                "質問5",
                "質問6",
                "質問7",
                "質問8",
                "質問9"],
     "カテゴリー2": ["占いは信じるほうだ",
                "3次元ではないキャラクターでもいつか会って会話をしている自分が想像できる",
                "最初否定していたコンテンツに、なにかのきっかけでどっぷり沼ってしまう",
                "質問13",
                "質問14"
                ,"質問15"
                ,"質問17"
                ,"質問18"],
     "カテゴリー3": ["接触イベントでのファン対応が良い人が好き",
                "推しの交友関係の中で素行が悪い人がいると心配になる",
                "「推しのグッズは絶対に手に入れたい」",
                "質問22",
                "質問23",
                "質問24",
                "質問25",
                "質問26",
                "質問27"],
     "カテゴリー4": ["推しに熱愛が出たら即座に降りる"
                , "推しに熱愛が出たら即座に降りる",
                "推しに熱愛が出たら即座に降りる",
                "質問28",
                "質問29",
                "質問30",
                "質問31"
                ,質問32",
                "質問33",]
                
}

responses = []  # 初期化を追加

for category, questions in categories.items():
    for idx, q in enumerate(questions):
        col1, col2 = st.columns([2, 3])  # 質問とラジオボタンを横並びにする
        with col1:
            st.write(f"**{q}**")  # 質問を左に配置
        with col2:
            # ユニークなキーを作成するために、category と質問のインデックスを追加
            response = st.radio("", ["当てはまる", "当てはまらない", "どちらでもない", "意味が分からない"], 
                                key=f"{category}_{idx}", horizontal=True)  # 4択に変更
            responses.append(response)

        # 質問と質問の間に改行を入れる
        st.markdown("<br>", unsafe_allow_html=True)  # 改行タグを使って1行空ける


if st.button("診断を実行"):
    result_I_E = calculate_result(responses[0:3], "I", "E")
    result_S_N = calculate_result(responses[3:6], "S", "N")
    result_T_F = calculate_result(responses[6:9], "T", "F")
    result_J_P = calculate_result(responses[9:12], "J", "P")

    final_result = f"{result_I_E}{result_S_N}{result_T_F}{result_J_P}"
    st.session_state["final_result"] = final_result

    # 現在の日時を取得
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 解答内容を一緒に記録する
    try:
        # ユーザーの解答と診断結果をスプレッドシートに記録
        sheet.append_row([now, result_I_E, result_S_N, result_T_F, result_J_P, final_result] + responses)
        st.success("診断結果と解答がスプレッドシートに記録されました！")
    except Exception as e:
        st.error(f"スプレッドシートへの記録に失敗しました: {e}")

# 診断結果のページに遷移
    st.switch_page(f"pages/{final_result}.py")
