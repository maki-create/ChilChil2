import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Streamlit Secretsから情報を取得
google_credentials = st.secrets["google_credentials"]

# TOMLの設定情報を辞書として利用
creds_dict = {
    "type": "service_account",
    "project_id": "aerial-antonym-444302-f9",
    "private_key_id": "e820019c59356e62d1609fe32a5543a8bb810146",
    "private_key": 
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCgZ7G8aGzl4rhFIPgWfBqxblSd/dAI1cuPXQsQ5ruHT7WjBSzo0r5Hb+o3WhyWcDTftGcQ6ESm4jNxN5ErKAl9NWet80oarv18E4Iq0aAGNH24V2FcWBuRqBAFVJzVaPSOcwwieyVxDcb6zpZViTFxqG0I/5unKOhF50rLCpFMNU6Ls5HtZU/+Sz0f1/99nUbhWa8Nr/OUxK8QoVGVIGFJ+V0tcbEi8ED3EtCxpcAe7NoAciUxrn2ngV43kRgrLWSoIjeokmgKhSelfR4WMKdqSyyv+oxHKJqGrYvtOsqn/q/FWIzEpqKGx768/5tG68XaPFvXiUiM6TIta7I03oOrAgMBAAECggEAIkJzgj+1fpYhcFZd1oOUOfBML2BuBe0P6KNhQS9ev0RFkbeBw4p7bIuZNVBQSctWZ69C0ighvZkTjqtlHJgVCsKUzeDoI3HbnxwVkaqrKJgef/hdyZjh7oa8QT80rhoYHbKx1U2DDjX4mUn1bvh58IIeI61gY+AHWCLR5TLxHJrxUfhD+wgV7y66ZxQrdKML1qWbIlnJkY6m4sg1Voj4r+nUKAKaiwa22CVclE7sErSMbC1u8cHpvdXOYWJZDD5199OVf2yIe4HfqWBC2S5yJKhRZuG6xPsLPS99QZdgCEOg2DWK+ExIb8Rj5bp/7fi6IHuJzNrx7BNrK5BJ55ukYQKBgQDZMUsqczw4CKMO2NKfXz6rHMQrmIN/9mLp9SlCYnaub5M3MedE0ulll1AdVgSqqEEkzqjP1xq8XXMJDU+mxY0SkxBBEDlHETU/M6R5FN8ZTmcxDc2fQdB4kQe9e6cygPvzpA1DuiIlF2/0Vg8SI6b/3IiG3vj0BsixT0CBzGDAywKBgQC9ENtsrMrXiniux4JHiFqq6rMEg8KydAxMJStodkMvUiVUuReTk6CWWqBw9Oi+AzEfodh+JNZtcrPOs3SUh0cfFAbYxlgpRGZyMVeqo6MU2eLnHmam+rjG2UurlVjuIFdm16V7uQa/u0gtkBLJvn5WDwKNOaivnvdgSU5qDDtMoQKBgHAMQCzsOjrmKcj1DuPtbRU1x/Z9vgl8ANeWBO0cgwHGyfoForwc2w/wGgKoZ8vq9YCZpPlkjYRz6W7YESmGbRsSB6apSgNh20h5yfY1UEtr6UyjRFtOxtAMciPM8Rra9CBjl/xCwG7GQpmY9Dl1byg8i6qYyXKLNWpT6oGMALY1AoGBAIPYK4w/ezyP3dTUYC+OENw7yxcM40sazjCTgw/X2MY5HLtWT/Cj9EqlbFkZEOzgwPL0JErjWXz9jhJI5rVlGN29U4D74CL3BhIAAsiGUIWL5EWT17X+Bbj1c2V2Qovcldar70S2JNSzv4O2gsOZSfSthvQBD3dY/d1xgXNGkFvBAoGBAJVybo+dJBe10tDIsxSZ4rtQePhxF8VrzMtIOybA+G3678cVvOCjrOP2Ho/U41iQTzy6uW4b3ajAID4djV82R44pR/9b16efpB7JGfePTShXF6tIGQKLKDKQ6aJUIELIFNnLbfzhmDE0w7cxEeSbOCJ3Uf6rsJ26o4E1rNwdpWrE,
    "client_email": "service-account@aerial-antonym-444302-f9.iam.gserviceaccount.com",
    "client_id": "100259023955694299607",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/service-account%40aerial-antonym-444302-f9.iam.gserviceaccount.com"
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
    "コンテンツ1": ["質問 1", "質問 2", "質問 3"],
    "コンテンツ2": ["質問 4", "質問 5", "質問 6"],
    "コンテンツ3": ["質問 7", "質問 8", "質問 9"],
    "コンテンツ4": ["質問 10", "質問 11", "質問 12"]
}

responses = []

for category, questions in categories.items():
    st.subheader(f"{category}")
    for q in questions:
        col1, col2 = st.columns([2, 3])  # 質問とラジオボタンを横並びにする
        with col1:
            st.write(f"**{q}**")  # 質問を左に配置
        with col2:
            response = st.radio("", ["当てはまる", "当てはまらない", "どちらでもない", "意味が分からない"], key=f"{category}_{q}", horizontal=True)  # 4択に変更
            responses.append(response)

if st.button("診断を実行"):
    result_I_E = calculate_result(responses[0:3], "I", "E")
    result_S_N = calculate_result(responses[3:6], "S", "N")
    result_T_F = calculate_result(responses[6:9], "T", "F")
    result_J_P = calculate_result(responses[9:12], "J", "P")

    final_result = f"{result_I_E}{result_S_N}{result_T_F}{result_J_P}"
    st.session_state["final_result"] = final_result

    # 現在の日時を取得
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # スプレッドシートに診断結果を書き込む
    try:
        sheet.append_row([now, result_I_E, result_S_N, result_T_F, result_J_P, final_result])
        st.success("診断結果がスプレッドシートに記録されました！")
    except Exception as e:
        st.error(f"スプレッドシートへの記録に失敗しました: {e}")

    # 診断結果のページに遷移
    st.switch_page(f"pages/{final_result}.py")
