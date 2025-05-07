import os
import uuid
import requests
from dotenv import load_dotenv
from openai import OpenAI
from django.core.files.base import ContentFile
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import History
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings

# .env から API キーを読み込む
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# たとえ話を生成
def generate_metaphor(prompt_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"{prompt_text} をたとえ話で説明してください。200文字以内でお願いします。"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# イラスト用プロンプトを作成
def convert_metaphor_to_image_prompt(metaphor_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": f"次のたとえ話をもとに、DALL·Eがイラスト化しやすいようなプロンプトに変換してください：\n\n{metaphor_text}\n\n日本語で100文字以内でお願いします。"}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

# 画像を生成
def generate_image(prompt_text):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"イラスト風。{prompt_text} をわかりやすく図で説明した構成。アイコン化、単純なスタイルで。",
        size="1024x1024",
        n=1
    )
    return response.data[0].url

# 画像URLからローカルに保存
def save_image_from_url(image_url, filename):
    response = requests.get(image_url)
    return ContentFile(response.content, name=filename)

# フォーム送信後の処理
@csrf_exempt
def generate_all(request):
    prompt = request.POST.get("prompt", "")
    metaphor = generate_metaphor(prompt)
    image_prompt = convert_metaphor_to_image_prompt(metaphor)
    image_url = generate_image(image_prompt)

    # ファイル名を一意にして保存
    filename = f"{uuid.uuid4().hex}.png"
    image_file = save_image_from_url(image_url, filename)

    # DBに履歴を保存
    entry = History(prompt=prompt, metaphor=metaphor)
    entry.image.save(filename, image_file)
    entry.save()

    return render(request, 'metaphor/result_fragment.html', {
        'metaphor': metaphor,
        'image_url': entry.image.url,
    })

# 履歴ページ表示
def history(request):
    records = History.objects.order_by('-created_at')
    return render(request, 'metaphor/history.html', {'records': records})

def delete_history(request, pk):
    history = get_object_or_404(History, pk=pk)
    
    # ファイルも削除
    if history.image and os.path.isfile(history.image.path):
        os.remove(history.image.path)

    history.delete()
    return redirect('history')

# 最初の入力フォーム画面
@csrf_exempt
def index(request):
    return render(request, 'metaphor/index.html')
