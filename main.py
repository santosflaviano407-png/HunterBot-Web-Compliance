import os
import random
import time
import requests

# --- CONFIGURAÇÃO DE CREDENCIAIS PROTEGIDAS DA NUVEM ---
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM')
CHAT_ID_TELEGRAM = os.environ.get('CHAT_ID_TELEGRAM', '7726228493')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# ESCOPO DE AUDITORIA: Portais de Teste Comerciais
empresas_alvo = ["uol.com.br", "terra.com.br", "globo.com"]

print("--- 🤖 INICIANDO HUNTERBOT PRO COM INTELIGÊNCIA ARTIFICIAL ---")

# URL Oficial da API de Bots do Telegram
url_telegram = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"

def pedir_analise_ia(empresa, elemento_ti):
    """Conecta o robô à API do Gemini focado em boas práticas de infraestrutura de TI"""
    url_gemini = f"https://googleapis.com{GEMINI_API_KEY}"
    
    prompt = (
        f"Atue como um analista sênior de infraestrutura web. O site '{empresa}' "
        f"pode implementar melhorias ativando o parâmetro de cabeçalho '{elemento_ti}'. "
        f"Explique de forma muito curta (máximo 3 linhas) o benefício técnico desse parâmetro "
        f"para a proteção dos dados dos clientes e como o administrador configura no Nginx."
    )
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        resposta = requests.post(url_gemini, json=payload, timeout=10)
        dados = resposta.json()
        
        # Extração correta utilizando chaves e índices válidos
        texto_ia = dados['candidates'][0]['content']['parts'][0]['text']
        return texto_ia
    except Exception as e:
        return f"Aviso técnico: IA retornou formato inesperado. Log interno: {e}"

for empresa in empresas_alvo:
    url = f"https://{empresa}"
    print(f"\n[ Mapeando Borda ] {url}...")
    try:
        resposta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=7)
        response_headers = resposta.headers
        
        # Identificação de melhorias de Infraestrutura e Conformidade
        mejorias_necessarias = []
        if "Content-Security-Policy" not in response_headers:
            mejorias_necessarias.append("Content-Security-Policy (CSP)")
        if "X-Frame-Options" not in response_headers:
            mejorias_necessarias.append("X-Frame-Options (Proteção de Interface)")
        if "X-Content-Type-Options" not in response_headers:
            mejorias_necessarias.append("X-Content-Type-Options (MIME Guard)")
        if "Strict-Transport-Security" not in response_headers:
            mejorias_necessarias.append("Strict-Transport-Security (HSTS)")
            
        if mejorias_necessarias:
            print(f" -> [INFO] {empresa} aceita {len(mejorias_necessarias)} otimizações! Consultando Gemini...")
            for item in mejorias_necessarias:
                analise_da_ia = pedir_analise_ia(empresa, item)
                
                # Montagem linear e alinhamento em 16 espaços exatos
                mensagem_final = f"🧠 *CONSULTORIA DE IA: HUNTERBOT & GEMINI*\n\n⚠️ *Alvo:* {empresa}\n❌ *Otimização:* {item}\n\n🛡️ *Parecer Técnico da IA:*\n{analise_da_ia}"
                
                # Envio e pausas do loop interno
                requests.post(url_telegram, data={"chat_id": CHAT_ID_TELEGRAM, "text": mensagem_final, "parse_mode": "Markdown"}, timeout=5)
                time.sleep(1)
            print(f"[+] Análise de {empresa} concluída.")
    except Exception as e:
        print(f"[-] Erro ao processar o alvo {empresa}: {e}")
    time.sleep(3)

print("\n--- 🌟 VARREDURA COM INTELIGÊNCIA ARTIFICIAL FINALIZADA! ---")
