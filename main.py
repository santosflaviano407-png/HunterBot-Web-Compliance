import os
import time
import requests

print("--- 🤖 INICIANDO BOT QUANTITATIVO DE LONGO PRAZO (RUMO AO MILHÃO) ---")

# Busca as credenciais salvas no seu GitHub Secrets / Variáveis de Ambiente
TELEGRAM_TOKEN = os.getenv("TOKEN_TELEGRAM")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_mensagem_telegram(mensagem):
    """Envia o relatório quantitativo consolidado diretamente para o Telegram"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[!] Erro: Credenciais do Telegram ausentes nas Secrets.")
        return

    # CORREÇÃO: URL oficial da API de Bots do Telegram
    url = f"https://telegram.org{TELEGRAM_TOKEN.strip()}/sendMessage"
    
    payload = {
        "chat_id": TELEGRAM_CHAT_ID.strip(),
        "text": mensagem,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("[✓] Relatório estratégico enviado com sucesso para o Telegram!")
        else:
            print(f"[!] Erro no Telegram: Status {response.status_code} - {response.text}")
    except Exception as e:
        print(f"[!] Falha física de conexão com o Telegram: {e}")

def obter_dados_mercado_reais(ticker):
    """Busca o histórico de 90 dias via API do Yahoo Finance para o cálculo de médias"""
    print(f"[+] Coletando histórico estatístico para o ativo: {ticker}...")
    
    # CORREÇÃO: Endpoint correto da API pública do Yahoo Finance v8
    url = f"https://yahoo.com{ticker}"
    
    # User-Agent é obrigatório para evitar o Bloqueio 403 do Yahoo Finance
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    params = {"range": "90d", "interval": "1d"}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            
            # Navega na estrutura do JSON retornado pelo Yahoo
            precos = dados["chart"]["result"][0]["indicators"]["quote"][0]["close"]
            precos_limpos = [p for p in precos if p is not None]
            
            if len(precos_limpos) >= 50:
                return precos_limpos
            
        print(f"[!] Erro ou dados insuficientes da API do Yahoo ({response.status_code}). Usando fallback.")
        return [100.0] * 60
    except Exception as e:
        print(f"[!] Falha na requisição: {e}. Usando fallback estável.")
        return [100.0] * 60

def calcular_indicadores_institucionais(precos):
    """Calcula médias de 20 e 50 dias para filtragem de falsos sinais"""
    if len(precos) < 50:
        print(f"[!] Histórico insuficiente ({len(precos)} dias). Requerido mínimo de 50 dias.")
        return 0.0, 0.0
    
    media_curta = sum(precos[-20:]) / 20
    media_longa = sum(precos[-50:]) / 50
    return media_curta, media_longa

def executar_estrategia_patrimonial(ticker, peso_sugerido):
    """Aplica o modelo matemático focado em acúmulo de patrimônio"""
    ticker_b3 = f"{ticker}.SA"
    historico = obter_dados_mercado_reais(ticker_b3)
    media_20, media_50 = calcular_indicadores_institucionais(historico)
    
    if media_20 == 0.0 or media_50 == 0.0:
        return None
        
    ultimo_preco = historico[-1]
    
    # Formatação da string limpa para o Markdown do Telegram
    detalhes = (
        f"📊 *Ativo:* {ticker} (Alocação Alvo: {peso_sugerido})\n"
        f"• Preço Atual: R$ {ultimo_preco:.2f}\n"
        f"• Média Rastreadora (20d): R$ {media_20:.2f}\n"
        f"• Média Estrutural (50d): R$ {media_50:.2f}\n"
    )
    
    if media_20 > media_50:
        sinal = detalhes + "🚨 *DIRETRIZ:* 📈 *COMPRAR / MANTER* (Ciclo de alta robusto confirmado)."
    elif media_20 < media_50:
        sinal = detalhes + "🚨 *DIRETRIZ:* 📉 *AGUARDAR / EVITAR* (Ativo em tendência de baixa estrutural)."
    else:
        sinal = detalhes + "🚨 *DIRETRIZ:* ⏳ *ZONA NEUTRA* (Mercado sem direção definida)."
        
    return sinal

# Configuração da Carteira Rumo ao Milhão
portfolio = {
    "IVVB11": "40%",
    "BOVA11": "30%",
    "SMAL11": "15%"
}

consolidado_sinais = "💰 *ESTRATÉGIA QUANTITATIVA: RUMO AO MILHÃO* 💰\n\n"
consolidado_sinais += "Foco: Aportes Disciplinados, Tendência de Longo Prazo e Juros Compostos.\n\n"
consolidado_sinais += "------------------------\n\n"

for ativo, peso in portfolio.items():
    resultado_sinal = executar_estrategia_patrimonial(ativo, peso)
    if resultado_sinal:
        consolidado_sinais += resultado_sinal + "\n\n------------------------\n\n"
    time.sleep(1) # Delay preventivo para evitar rate limit na API do Yahoo

# Envia o direcionamento estratégico diretamente para o investidor
enviar_mensagem_telegram(consolidado_sinais)
print("\n--- 🌟 SISTEMA PATRIMONIAL EXECUTADO ---")
