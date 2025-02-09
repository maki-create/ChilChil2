from django.shortcuts import render
from .forms import SearchForm
from drive_api import get_all_files

def search_files(request):
    keyword = request.GET.get('keyword', '')

    # Google Drive API から全ファイル取得
    files = get_all_files()

    # 取得したデータを確認
    print("取得したファイル一覧:", files)  # ターミナルに出力

    # キーワード検索を適用
    filtered_files = [file for file in files if keyword.lower() in file['name'].lower()]
    
    return render(request, 'search_results.html', {'files': filtered_files})