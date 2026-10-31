import time
import os
import requests

print("--- 🤖 INICIANDO BOT QUANTITATIVO DE ANÁLISE PREDITIVA ---")

def obter_dados_mercado(ticker):
    """
    Simula e calcula dados de mercado para análise técnica.
    Em ambiente local, você pode usar a biblioteca 'yfinance' para puxar dados reais.
    """
    print(f"[+] Coletando histórico de preços para o ativo: {ticker}...")
    
    # Preços históricos fictícios simulando uma tendência estruturada para o teste
    precos_fechamento = [100.0, 101.5, 100.8, 102.3, 103.1, 102.9, 104.2, 105.0, 104.8, 106.1]
    return precos_fechamento

def calcular_indicadores(precos):
    """Calcula médias móveis e momentum estatístico dos preços"""
    if len(precos) < 3:
        return 0.0, 0.0
    
    # Média curta dos últimos 3 dias
    media_curta = sum(precos[-3:]) / 3
    # Média longa dos últimos 5 dias
    media_longa = sum(precos[-5:]) / 5
    
    return media_curta, media_longa

def executar_estrategia(ticker):
    """Aplica a lógica quantitativa para gerar o sinal de trade"""
    historico = obter_dados_mercado(ticker)
    
    # CORREÇÃO AQUI: Chamada limpa da função
    media_curta, media_longa = calcular_indicadores(historico)
    ultimo_preco = historico[-1]
    
    print(f"📊 Último Preço: R$ {ultimo_preco:.2f} | Média Curta: R$ {media_curta:.2f} | Média Longa: R$ {media_longa:.2f}")
    
    # Regra de Cruzamento de Médias (Golden Cross / Death Cross simplificado)
    if media_curta > media_longa:
        sinal = "📈 COMPRA: Tendência de Alta confirmada por indicadores quantitativos."
    elif media_curta < media_longa:
        sinal = "📉 VENDA: Indicadores apontam perda de força e possível queda."
    else:
        sinal = "⏳ AGUARDAR: Mercado lateralizado, sem tendência clara definida."
        
    return sinal

# Loop Principal de Varredura de Ativos
ativos_alvo = ["BOVA11", "IVVB11", "SMAL11"]

for ativo in ativos_alvo:
    print("-" * 50)
    resultado_sinal = executar_estrategia(ativo)
    print(f"🚨 SINAL DO BOT PARA {ativo}: {resultado_sinal}")
    time.sleep(2)

print("\n--- 🌟 ANÁLISE QUANTITATIVA FINALIZADA COM SUCESSO ---")
