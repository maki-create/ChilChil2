import os
import json
from oauth2client.service_account import ServiceAccountCredentials

# Streamlit Secretsから情報を取得
google_credentials = st.secrets["google_credentials"]

# TOMLの設定情報を辞書として利用
creds_dict = {
    "type": google_credentials["type"],
    "project_id": google_credentials["project_id"],
    "private_key_id": google_credentials["private_key_id"],
    "private_key": google_credentials["private_key"],
    "client_email": google_credentials["client_email"],
    "client_id": google_credentials["client_id"],
    "auth_uri": google_credentials["auth_uri"],
    "token_uri": google_credentials["token_uri"],
    "auth_provider_x509_cert_url": google_credentials["auth_provider_x509_cert_url"],
    "client_x509_cert_url": google_credentials["client_x509_cert_url"],
}

# Google Sheets API認証を設定
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets APIの認証情報を設定
creds_path = "C:/Users/81908/Downloads/aerial-antonym-444302-f9-9ff7a2c99cca.json"  # 認証JSONのパス
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)

# Googleスプレッドシートを開く（シートのURLまたはIDを指定）
spreadsheet_id = "1eKhD929QC8fdvse2G92woknfWh7Dnv7Pmi2w1ZqXWCM"  # ★ここにスプレッドシートのIDを入れる
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

# スコア計算関数
def calculate_result(answers, label1, label2):
    score1 = sum(1 for ans in answers if ans == '〇')
    score2 = sum(1 for ans in answers if ans == '×')

    if score1 > score2:
        return label1
    elif score2 > score1:
        return label2
    else:
        return f"{label1}, {label2}"

# Streamlit UI
st.title("性格診断アプリ")
st.write("各質問に対して「〇」または「×」を選んでください。")

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
            response = st.radio("", ["〇", "×"], key=f"{category}_{q}", horizontal=True)  # 選択肢を横並びに
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
    sheet.append_row([now, result_I_E, result_S_N, result_T_F, result_J_P, final_result])

    # 診断結果のページに遷移
    st.switch_page(f"pages/{final_result}.py")
