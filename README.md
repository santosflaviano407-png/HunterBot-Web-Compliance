# HunterBot: Analisador Automático de Postura e Conformidade Web

Este projeto consiste em um microsserviço automatizado em Python projetado para auditar de forma 100% passiva a presença de cabeçalhos de segurança HTTP e conformidade de cookies em escopos web corporativos.

## 🚀 Funcionamento Autônomo (SaaS)
A ferramenta está totalmente integrada ao **GitHub Actions**, utilizando rotinas de agendamento virtual (*Cron Jobs*) para executar varreduras diárias de forma independente, disparando relatórios de severidade em tempo real via API para o Telegram.

### Defesas Monitoradas:
- **Postura Global:** Presença de políticas de restrição de scripts `Content-Security-Policy` (CSP).
- **Assinatura de Infraestrutura:** Mapeamento de servidores ativos (Ex: Nginx, Apache, Cloudflare).
- **Controle Ético:** Mecanismo de *Throttling* para respeito à largura de banda e limite de requisições dos alvos.

## 🛠️ Tecnologias
- Python 3
- Biblioteca Requests
- GitHub Actions (Automação em Nuvem)
- API de Mensagens do Telegram

## 🔒 Segurança de Credenciais
O projeto segue rígidos padrões profissionais de desenvolvimento (DevSecOps). Todos os tokens confidenciais e chaves de API estão protegidos em variáveis de ambiente criptografadas (*Repository Secrets*), mantendo o código público totalmente seguro para fins de portfólio.
