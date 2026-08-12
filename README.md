# CVE Monitor

Um monitor de CVEs (Common Vulnerabilities and Exposures) que envia notificações via Telegram sobre novas vulnerabilidades publicadas no National Vulnerability Database (NVD), uma forma de se manter atualizado.

## Características

- Monitoramento automático de novas CVEs
- Notificações via Telegram
- Configuração flexível de intervalos de verificação
- Limitação personalizável de CVEs por dia
- Score CVSS incluído nas notificações
- Logging detalhado das operações

## Pré-requisitos

- Python 3.7+
- Token de bot do Telegram
- ID do chat do Telegram onde as mensagens serão enviadas

## Instalação

1. Clone o repositório:
```
git clone https://github.com/MaximilianoMeyer/cve-monitor.git
cd cve-monitor
```

2. Instale as dependências:
```
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente criando um arquivo `.env` na raiz do projeto:
```env
TELEGRAM_TOKEN=seu_token_do_telegram
TELEGRAM_CHAT_ID=seu_chat_id
CHECK_INTERVAL=3600  # opcional, padrão: 3600 segundos (1 hora)
MESSAGE_DELAY=2      # opcional, padrão: 2 segundos

```

## Uso

1. Execute o script:
```
python cve_monitor.py
```

2. Digite a quantidade de CVEs que deseja receber.

3. O monitor começará a verificar novas CVEs automaticamente e enviará notificações via Telegram.

## Formato das Notificações

As notificações incluem:
- ID da CVE
- Score CVSS (se disponível)
- Descrição da vulnerabilidade
- Link para mais detalhes no NVD

Exemplo:
```
🚨 Nova CVE Detectada 🚨

ID: CVE-2024-XXXX
CVSS Score: 7.5
Descrição: Descrição da vulnerabilidade...
Link: https://nvd.nist.gov/vuln/detail/CVE-2024-XXXX
