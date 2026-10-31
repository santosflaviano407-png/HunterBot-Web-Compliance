import os
import time
import requests

# --- CONFIGURAÇÃO DE CREDENCIAIS PROTEGIDAS DA NUVEM ---
TOKEN_TELEGRAM = os.environ.get('TOKEN_TELEGRAM')
CHAT_ID_TELEGRAM = 7726228493
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# 🎯 ESCOPO DE AUDITORIA: Substitua 'seu-site.com.br' pelo domínio da sua página real!
empresas_alvo = ["uol.com.br", "terra.com.br", "globo.com"]

print("--- 🤖 INICIANDO HUNTERBOT PRO COM INTELIGÊNCIA ARTIFICIAL ---")

# URL oficial da API de Bots do Telegram
url_telegram = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"

def pedir_analise_ia(empresa, falha):
    """Conecta o robô à API do Gemini para gerar pareceres técnicos de cibersegurança"""
    url_gemini = f"https://generativelanguage.googleapis.comv1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = (
        f"Você é um especialista em cibersegurança sênior. O meu scanner detectou que o site '{empresa}' "
        f"está vulnerável porque falta o cabeçalho de proteção '{falha}'. Explique de forma muito curta (máximo 3 linhas) "
        f"qual é o risco real dessa falha e como o programador corrige isso de forma simples no servidor."
    )
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        resposta = requests.post(url_gemini, json=payload, timeout=10)
        dados = resposta.json()
        texto_ia = dados['candidates'][0]['content']['parts'][0]['text']
        return texto_ia
    except Exception as e:
        return f"Aviso: IA em manutenção. Detalhe técnico: {e}"

for empresa in empresas_alvo:
    url = f"https://{empresa}"
    print(f"\n[ Mapeando Borda ] {url}...")
    
    try:
        resposta = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=7)
        headers = response_headers = resposta.headers
        
        # Mapeamento das 4 falhas críticas de segurança web
        falhas_detectadas = []
        
        if "Content-Security-Policy" not in response_headers:
            falhas_detectadas.append("Content-Security-Policy (CSP)")
            
        if "X-Frame-Options" not in response_headers:
            falhas_detectadas.append("X-Frame-Options (Proteção Clickjacking)")
            
        if "X-Content-Type-Options" not in response_headers:
            falhas_detectadas.append("X-Content-Type-Options (Sniffing Mitigate)")
            
        if "Strict-Transport-Security" not in response_headers:
            falhas_detectadas.append("Strict-Transport-Security (HSTS Encryption)")

        # Se encontrar qualquer uma das falhas, o robô processa os relatórios com a IA
        if falhas_detectadas:
            print(f"   -> [ALERTA] {empresa} possui {len(falhas_detectadas)} inconformidades! Acionando Gemini...")
            
            for falha in falhas_detectadas:
                analise_da_ia = pedir_analise_ia(empresa, falha)
                
                # Monta a mensagem estruturada final para o cliente
                mensagem_final = (
                    f"🧠 *CONSULTORIA DE IA: HUNTERBOT PRO*\n\n"
                    f"⚠️ *Alvo:* {empresa}\n"
                    f"❌ *Inconformidade:* {falha}\n\n"
                    f"🛡️ *Parecer Técnico do Especialista Gemini:*\n{analise_da_ia}"
                )
                
                requests.post(url_telegram, data={"chat_id": CHAT_ID_TELEGRAM, "text": mensagem_final, "parse_mode": "Markdown"}, timeout=5)
                time.sleep(2) # Pausa estratégica para o Telegram não bloquear por flood
                
        print(f"[+] Análise de {empresa} concluída.")
        
    except Exception as e:
        print(f"[-] Servidor offline ou recusou conexão em {url}: {e}")
        
    time.sleep(3)

print("\n--- 🌟 VARREDURA AVANÇADA FINALIZADA COM SUCESSO! ---")
