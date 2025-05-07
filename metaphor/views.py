# Create your views here.
import os
from openai import OpenAI
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from dotenv import load_dotenv

import time

load_dotenv()  # ← これを忘れると .env が読み込まれません
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # .env推奨


api_key = os.getenv("OPENAI_API_KEY")
print("✅ API KEY:", api_key)  # ← こう書く

client = OpenAI(api_key=api_key)


def generate_metaphor(prompt_text):
    response = client.chat.completions.create(  # ← client で呼び出すのが正解
        model="gpt-4",  # または "gpt-3.5-turbo"
        messages=[
            {"role": "user", "content": f"{prompt_text} をたとえ話で説明してください。200文字以内でお願いします。"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

def generate_image(prompt_text):
    response = client.images.generate(
        model="dall-e-3",  # v1系では明示的にモデル名を指定
        prompt=f"イラスト風。{prompt_text} をわかりやすく図で説明した構成。アイコン化、単純なスタイルで。",
        size="1024x1024",  # dall-e-3でサポートされているサイズは、"1024x1024"(通常のサムネイル・SNS用など)、"1792x1024"(モバイル、書籍、図解向け)、"1024x1792"(横長バナーやスライド向け)
        n=1              # 1枚生成
    )
    return response.data[0].url  # ← URLで返ってくる

def convert_metaphor_to_image_prompt(metaphor_text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": f"次のたとえ話をもとに、DALL·Eがイラスト化しやすいようなプロンプトに変換してください：\n\n{metaphor_text}\n\n日本語で100文字以内でお願いします。"
            }
        ],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

@csrf_exempt
def index(request):
    return render(request, 'metaphor/index.html')

@csrf_exempt
def generate_all(request):
    prompt = request.POST.get("prompt", "")
    metaphor = generate_metaphor(prompt)
    image_prompt = convert_metaphor_to_image_prompt(metaphor)
    image_url = generate_image(image_prompt)
    return render(request, 'metaphor/result_fragment.html', {
        'metaphor': metaphor,
        'image_url': image_url,
    })