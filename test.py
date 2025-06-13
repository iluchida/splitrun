# test.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# 環境変数の読み込み（.env ファイルに API キーがある場合）
load_dotenv()

# Gemini API キーの設定
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 利用可能なモデル一覧を表示
for model in genai.list_models():
    print(model.name)

# # test.py
# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# # .envファイルからAPIキー読み込み
# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY が .env に設定されていません")

# # Gemini APIの初期化
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel("gemini-pro")

# # テストプロンプト
# prompt = "こんにちは、あなたは誰？"
# response = model.generate_content(prompt)

# print("▼ Geminiの回答：")
# print(response.text)
