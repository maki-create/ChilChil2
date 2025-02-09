import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os



# --- Excelファイルを処理 ---
def process_sheet(file_path):
    if not os.path.exists(file_path):
        print(f"Error: ファイルが見つかりません: {file_path}")
        return

    # Excelファイルを読み込む
    sheet = pd.read_excel(file_path, sheet_name=0)
    print("Initial sheet loaded:")
    print(sheet)

    # A列で重複を削除（最初の1つを残す）
    sheet = sheet.drop_duplicates(subset=sheet.columns[0], keep='first').reset_index(drop=True)
    print("Sheet after removing duplicates in A column:")
    print(sheet)

    # 加工後のExcelファイルを保存
    output_path = file_path.replace('.xlsx', '_processed.xlsx')
    sheet.to_excel(output_path, index=False)
    print(f"\nProcessed file saved to {output_path}")

    return sheet  # 加工したデータフレームを返す

# --- Google Sheetsにデータをアップロード ---
def upload_to_google_sheets(df, client, sheet_id, sheet_name):
    try:
        # Google Sheetsに接続
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.clear()  # 既存のデータをクリア

        # データを一括アップロード
        data = [list(df.columns)] + df.values.tolist()  # ヘッダー + データ
        worksheet.update('A1', data)

        print(f"データをシート '{sheet_name}' にアップロードしました")
    except Exception as e:
        print(f"Google Sheetsアップロードエラー: {e}")

# --- スクリプトのエントリーポイント ---
if __name__ == "__main__":
   

    # Excelファイルを処理
    file_path = 'D:/python/output.xlsx'
    df = process_sheet(file_path)
    