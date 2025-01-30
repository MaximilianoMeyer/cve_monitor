import requests
import time
from datetime import datetime, timedelta, UTC
import json
import logging
from typing import List, Dict
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class CVEMonitor:
    def __init__(self, telegram_token: str, chat_id: str, max_cves_per_day: int = 10, 
                 check_interval: int = 3600, message_delay: int = 2):
        """
        Inicializa o monitor de CVEs
        
        Args:
            telegram_token (str): Token do bot do Telegram
            chat_id (str): ID do chat onde as mensagens serão enviadas
            max_cves_per_day (int): Número máximo de CVEs para enviar por dia
            check_interval (int): Intervalo entre verificações em segundos (padrão: 1 hora)
            message_delay (int): Delay entre mensagens em segundos (padrão: 2 segundos)
        """
        self.nvd_api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.telegram_api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        self.chat_id = chat_id
        self.check_interval = check_interval
        self.max_cves_per_day = max_cves_per_day
        self.message_delay = message_delay
        self.last_check_time = None
        
        # Configuração do logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def get_recent_cves(self) -> List[Dict]:
        """
        Busca CVEs recentes no NVD
        
        Returns:
            List[Dict]: Lista de CVEs encontradas
        """
        try:
            # Define o período de busca (últimas 24 horas)
            start_date = datetime.now(UTC) - timedelta(days=1)
            params = {
                'pubStartDate': start_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
                'pubEndDate': datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.000")
            }
            
            response = requests.get(self.nvd_api_url, params=params)
            response.raise_for_status()
            
            vulnerabilities = response.json().get('vulnerabilities', [])
            
            # Limita o número de CVEs conforme configurado
            return vulnerabilities[:self.max_cves_per_day]
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao buscar CVEs: {e}")
            return []

    def format_cve_message(self, cve: Dict) -> str:
        """
        Formata a mensagem da CVE para envio
        
        Args:
            cve (Dict): Dados da CVE
            
        Returns:
            str: Mensagem formatada
        """
        cve_data = cve['cve']
        cve_id = cve_data['id']
        description = cve_data['descriptions'][0]['value']
        
        # Obtém o CVSS v3 se disponível
        metrics = cve_data.get('metrics', {})
        cvss_v3 = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})
        cvss_score = cvss_v3.get('baseScore', 'N/A')
        
        message = (
            f"🚨 Nova CVE Detectada 🚨\n\n"
            f"ID: {cve_id}\n"
            f"CVSS Score: {cvss_score}\n"
            f"Descrição: {description}\n"
            f"Link: https://nvd.nist.gov/vuln/detail/{cve_id}"
        )
        
        return message

    def send_telegram_message(self, message: str) -> bool:
        """
        Envia mensagem via Telegram
        
        Args:
            message (str): Mensagem a ser enviada
            
        Returns:
            bool: True se enviado com sucesso, False caso contrário
        """
        try:
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': 'HTML'
            }
            
            response = requests.post(self.telegram_api_url, json=payload)
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao enviar mensagem no Telegram: {e}")
            return False

    def run(self):
        """
        Executa o monitor de CVEs em loop
        """
        self.logger.info("Iniciando monitor de CVEs...")
        
        while True:
            try:
                # Busca CVEs recentes
                cves = self.get_recent_cves()
                
                # Processa e envia notificações
                for i, cve in enumerate(cves, 1):
                    message = self.format_cve_message(cve)
                    if self.send_telegram_message(message):
                        self.logger.info(f"Notificação {i}/{self.max_cves_per_day} enviada para CVE: {cve['cve']['id']}")
                    
                    # Aplica o delay entre mensagens
                    if i < len(cves):
                        time.sleep(self.message_delay)
                    
                self.last_check_time = datetime.now(UTC)
                self.logger.info(f"Verificação concluída. Próxima verificação em {self.check_interval} segundos")
                
                # Aguarda até a próxima verificação
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.logger.error(f"Erro inesperado: {e}")
                time.sleep(60)  # Aguarda 1 minuto em caso de erro

def get_user_input():
    """
    Obtém input do usuário para quantidade de CVEs
    
    Returns:
        int: Número máximo de CVEs por dia
    """
    while True:
        try:
            user_input = input("Digite a quantidade de CVEs que deseja receber: ")
            max_cves = int(user_input)
            
            if max_cves <= 0:
                print("Por favor, digite um número maior que zero.")
                continue
                
            return max_cves
            
        except ValueError:
            print("Por favor, digite um número válido.")

if __name__ == "__main__":
    # Obtém as configurações das variáveis de ambiente
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', '3600'))  # valor padrão de 1 hora
    MESSAGE_DELAY = int(os.getenv('MESSAGE_DELAY', '2'))  # valor padrão de 2 segundos
    
    # Verifica se as variáveis obrigatórias estão definidas
    if not TELEGRAM_TOKEN or not CHAT_ID:
        raise ValueError("As variáveis de ambiente TELEGRAM_TOKEN e TELEGRAM_CHAT_ID são obrigatórias")
    
    # Obtém a quantidade de CVEs do usuário
    max_cves = get_user_input()
    
    # Inicia o monitor
    monitor = CVEMonitor(
        TELEGRAM_TOKEN, 
        CHAT_ID, 
        max_cves_per_day=max_cves,
        check_interval=CHECK_INTERVAL,
        message_delay=MESSAGE_DELAY
    )
    monitor.run()