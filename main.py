import os
import random
import time
import requests

# --- CONFIGURAÇÃO DE CREDENCIAIS PROTEGIDAS DA NUVEM ---
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM')
CHAT_ID_TELEGRAM = 7726228493
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Escopo de auditoria do programa
empresas_alvo = ["mercadolivre.com.br", "mercadolibre.com", "mercadopago.com", "adminml.com"]

print("--- 🤖 INICIANDO HUNTERBOT COM INTELIGÊNCIA ARTIFICIAL ---")

# URL oficial da API de Bots do Telegram
url_telegram = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"

def pedir_analise_ia(empresa, falha):
    """Conecta o robô à API do Gemini de forma assíncrona para enriquecimento de dados"""
    url_gemini = f"https://generativelanguage.googleapis.comv1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = (
        f"Você é um especialista em cibersegurança sênior. O meu scanner detectou que o site '{empresa}' "
        f"está vulnerável porque falta a proteção '{falha}'. Explique de forma muito curta (máximo 3 linhas) "
        f"qual é o risco real dessa falha para os usuários e como o programador corrige isso no servidor Nginx."
    )
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        resposta = requests.post(url_gemini, json=payload, timeout=10)
        dados = resposta.json()
        
        # Estrutura exata da árvore JSON da API do Gemini para capturar o texto puro
        texto_ia = dados['candidates'][0]['content']['parts'][0]['text']

        return texto_ia
    except Exception as e:
        return f"Aviso: IA em manutenção. Detalhe técnico: {e}"

for empresa in empresas_alvo:
    url = f"https://{empresa}"
    print(f"\n[ Mapeando Borda ] {url}...")
    
    try:
        resposta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=7)
        headers = resposta.headers
        
        # Monitoramento estrito de Content-Security-Policy (CSP)
        if "Content-Security-Policy" not in headers:
            print(f"   -> [ALERTA] {empresa} sem CSP! Solicitando parecer do consultor Gemini...")
            
            # O ROBÔ CHAMA A INTELIGÊNCIA ARTIFICIAL SOZINHO AQUI:
            analise_da_ia = pedir_analise_ia(empresa, "Content-Security-Policy (CSP)")
            
            # Monta o relatório estruturado final com a resposta da IA
            mensagem_final = (
                f"🧠 *CONSULTORIA DE IA: HUNTERBOT & GEMINI*\n\n"
                f"⚠️ *Alvo:* {empresa}\n"
                f"❌ *Inconformidade:* Ausência de CSP\n\n"
                f"🛡️ *Parecer Técnico da IA:*\n{analise_da_ia}"
            )
            
            requests.post(url_telegram, data={"chat_id": CHAT_ID_TELEGRAM, "text": mensagem_final, "parse_mode": "Markdown"}, timeout=5)
            
        print(f"[+] Análise de {empresa} concluída.")
        
    except Exception as e:
        print(f"[-] Servidor offline ou recusou conexão em {url}: {e}")
        
    time.sleep(3)

print("\n--- 🌟 VARREDURA COM INTELIGÊNCIA ARTIFICIAL FINALIZADA! ---")
