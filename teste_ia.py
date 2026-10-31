import os
import requests

key = os.environ.get("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent"
url = f"{base_url}?key={key}"

payload = {
    "contents": [{"parts": [{"text": "Diga a palavra OK se estiver funcionando."}]}]
}

try:
    resposta = requests.post(url, json=payload, timeout=10)
    dados = resposta.json()
    print("RESPOSTA COMPLETA DA IA:", dados)
except Exception as e:
    print("ERRO:", e)
