from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def count_words_view(request):
    if request.method == 'POST':
        # フォームからアップロードされたファイルと単語リストを取得
        uploaded_file = request.FILES.get('file')
        words_to_count = request.POST.get('words_to_count', '')

        # 必須のファイルまたは単語リストが不足している場合
        if not uploaded_file or not words_to_count:
            return HttpResponse("ファイルまたは単語リストが指定されていません。", status=400)
        
        # アップロードされたファイルの内容を読み取り（UTF-8としてデコード）
        text = uploaded_file.read().decode('utf-8')
        
        # 単語リストをカンマで分割してリスト化
        words_list = [word.strip() for word in words_to_count.split(',') if word.strip()]
        if not words_list:
            return HttpResponse("有効な単語が入力されていません。", status=400)

        # 各単語の出現回数をカウント
        word_counts = {word: text.count(word) for word in words_list}

        # 結果を文字列にまとめる
        result = "ワード出現回数:\n"
        for word, count in word_counts.items():
            result += f"{word}: {count}\n"

        # 結果をテキストファイルとしてダウンロードできるようにレスポンスを返す
        response = HttpResponse(result, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="word_count_results.txt"'
        return response
    
    # GETリクエスト時はファイルアップロードフォームを表示
    return render(request, 'count_words_form.html')
