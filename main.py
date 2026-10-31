import os
import random
import time
import requests

# --- CONFIGURAÇÃO DE CREDENCIAIS AUTOMÁTICAS ---
# O os.environ busca a chave secreta que guardamos na aba Settings
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM')
CHAT_ID_TELEGRAM = 7726228493

empresas_alvo = ["mercadolivre.com.br", "mercadolibre.com", "mercadopago.com", "adminml.com"]

print("--- 🤖 INICIANDO SCANNER AUTOMÁTICO INDEPENDENTE ---")

url_telegram = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"

for empresa in empresas_alvo:
    url = f"https://{empresa}"
    print(f"\n[ Mapeando Borda ] {url}...")
    
    try:
        resposta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=7)
        headers = resposta.headers
        
        servidor = headers.get("Server", "Protegido/Oculto")
        print(f"   -> [INFO] Servidor detectado: {servidor}")
        requests.post(url_telegram, data={"chat_id": CHAT_ID_TELEGRAM, "text": f"🔵 {empresa}: Servidor {servidor}"}, timeout=5)
        
        if "Content-Security-Policy" not in headers:
            print("   -> [ALERTA] Faltando política de CSP!")
            requests.post(url_telegram, data={"chat_id": CHAT_ID_TELEGRAM, "text": f"🔴 ALERTA: {empresa} sem CSP!"}, timeout=5)
            
        print(f"[+] Análise de {empresa} concluída.")
        
    except Exception as e:
        print(f"[-] Erro ao processar o alvo {empresa}: {e}")
        
    time.sleep(3)

print("\n--- 🌟 VARREDURA AUTOMÁTICA FINALIZADA COM SUCESSO! ---")
