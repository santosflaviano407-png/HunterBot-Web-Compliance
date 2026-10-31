import os
import requests
import time

key = os.environ.get("GEMINI_API_KEY")
base_url = "https://generativelanguage.googleapis.com/v1/models/gemini-3.8-flash:generateContent"
url = f"{base_url}?key={key}"

payload = {
    "contents": [{"parts": [{"text": "Diga a palavra OK se estiver funcionando."}]}]
}

# Configurações de retentativa
max_tentativas = 3
tempo_espera = 15  # Segundos de espera entre as tentativas

for tentativa in range(max_tentativas):
    try:
        resposta = requests.post(url, json=payload, timeout=30)
        
        # Se o servidor responder com 503 (Unavailable), força a queda no bloco 'except' para tentar de novo
        if resposta.status_code == 503:
            raise requests.exceptions.HTTPError("Servidor indisponível (503)")
            
        dados = resposta.json()
        print("RESPOSTA COMPLETA DA IA:", dados)
        break # Se deu certo, sai do loop imediatamente
        
    except (requests.exceptions.RequestException, Exception) as e:
        print(f"Tentativa {tentativa + 1} falhou devido a: {e}")
        if tentativa < max_tentativas - 1:
            print(f"Aguardando {tempo_espera} segundos antes de tentar novamente...")
            time.sleep(tempo_espera)
        else:
            print("Número máximo de tentativas atingido. O servidor continua fora do ar.")
