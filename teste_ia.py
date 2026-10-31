import os
import requests

key = os.environ.get("GEMINI_API_KEY")
url = f"https://googleapis.com{key}"

payload = {
    "contents": [{"parts": [{"text": "Diga a palavra OK se estiver funcionando."}]}]
}

try:
    resposta = requests.post(url, json=payload, timeout=10)
    dados = resposta.json()
    print("RESPOSTA DA IA:", dados["candidates"][0]["content"]["parts"][0]["text"])
except Exception as e:
    print("ERRO:", e)
