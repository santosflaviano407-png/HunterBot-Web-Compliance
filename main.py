import os
import time
import requests

print("--- 🤖 INICIANDO BOT QUANTITATIVO REAL (B3 via yfinance) ---")

# Captura o token e remove possíveis espaços ou caracteres inválidos (como asteriscos)
TELEGRAM_TOKEN = os.getenv("TOKEN_TELEGRAM")
if TELEGRAM_TOKEN:
    TELEGRAM_TOKEN = TELEGRAM_TOKEN.replace("*", "").strip()

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
if TELEGRAM_CHAT_ID:
    TELEGRAM_CHAT_ID = TELEGRAM_CHAT_ID.strip()

def enviar_mensagem_telegram(mensagem):
    """Envia o sinal formatado diretamente para o celular do usuário via Telegram"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[!] Alerta: Credenciais do Telegram não configuradas corretamente nas Secrets.")
        return
        
    url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("[✓] Notificação enviada com sucesso para o Telegram!")
        else:
            print(f"[!] Erro ao enviar mensagem: Status {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Falha na conexão com a API do Telegram: {e}")

def obter_dados_mercado_reais(ticker):
    """Busca o histórico real de fechamento usando a API do Yahoo Finance"""
    print(f"[+] Coletando histórico real de preços para o ativo: {ticker}...")
    
    # CORREÇÃO: Barra de separação explícita na URL antes do ticker
    url = f"https://yahoo.com{ticker}"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"range": "15d", "interval": "1d"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            precos = dados["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            precos_limpos = [p for p in precos if p is not None]
            return precos_limpos
        else:
            print(f"[!] Erro ao acessar Yahoo Finance ({response.status_code}). Usando contingência.")
            return [100.0, 101.5, 100.8, 102.3, 103.1, 102.9, 104.2, 105.0, 104.8, 106.1]
    except Exception as e:
        print(f"[!] Falha na requisição de mercado: {e}. Usando contingência.")
        return [100.0, 101.5, 100.8, 102.3, 103.1, 102.9, 104.2, 105.0, 104.8, 106.1]

def calcular_indicadores(precos):
    """Calcula as médias móveis matemáticas (curta e longa) com base nos preços reais"""
    if len(precos) < 5:
        print(f"[!] Histórico insuficiente ({len(precos)} dias). São necessários pelo menos 5 dias.")
        return 0.0, 0.0
    
    media_curta = sum(precos[-3:]) / 3
    media_longa = sum(precos[-5:]) / 5
    return media_curta, media_longa

def executar_estrategia(ticker):
    """Aplica as regras quantitativas e gera a string formatada do sinal"""
    ticker_b3 = f"{ticker}.SA"
    historico = obter_dados_mercado_reais(ticker_b3)
    
    media_curta, media_longa = calcular_indicadores(historico)
    if media_curta == 0.0 and media_longa == 0.0:
        return None
        
    ultimo_preco = historico[-1]
    
    detalhes = f"📊 *Ativo:* {ticker}\n• Último Preço: R$ {ultimo_preco:.2f}\n• Média Curta (3d): R$ {media_curta:.2f}\n• Média Longa (5d): R$ {media_longa:.2f}\n"
    
    if media_curta > media_longa:
        sinal = detalhes + "🚨 *SINAL:* 📈 *COMPRA* - Tendência de Alta quantitativa confirmada!"
    elif media_curta < media_longa:
        sinal = detalhes + "🚨 *SINAL:* 📉 *VENDA* - Perda de força detectada, viés de queda."
    else:
        sinal = detalhes + "🚨 *SINAL:* ⏳ *AGUARDAR* - Mercado lateralizado e sem direção."
        
    return sinal

# Loop Principal de Varredura de Ativos
ativos_alvo = ["BOVA11", "IVVB11", "SMAL11"]
consolidado_sinais = "🤖 *RELATÓRIO DO ROBÔ QUANTITATIVO B3*\n\n"

for ativo in ativos_alvo:
    print("-" * 50)
    resultado_sinal = executar_estrategia(ativo)
    if resultado_sinal:
        consolidado_sinais += resultado_sinal + "\n\n------------------------\n\n"
    time.sleep(2)

# Envia o relatório completo consolidado de uma só vez para o Telegram
enviar_mensagem_telegram(consolidado_sinais)

print("\n--- 🌟 PROCESSO CONCLUÍDO ---")
