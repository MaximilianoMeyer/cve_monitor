# monitors/cve_monitor.py
import requests
import logging
import time
from typing import List, Dict, Optional
from datetime import datetime, timedelta, UTC

class CVEMonitor:
    def __init__(self, telegram_token: str, chat_id: str, message_thread_id: int, 
                 github_token: Optional[str] = None,
                 max_cves_per_day: int = 10, 
                 check_interval: int = 18000, 
                 message_delay: int = 2):
        self.nvd_api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.telegram_api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        self.chat_id = chat_id
        self.message_thread_id = message_thread_id
        self.check_interval = check_interval
        self.max_cves_per_day = max_cves_per_day
        self.message_delay = message_delay
        self.last_check_time = None
        self.github_token = github_token
        self.github_headers = {"Authorization": f"token {github_token}"} if github_token else {}
        self.logger = logging.getLogger(__name__)

    def search_github_exploits(self, cve_id: str) -> List[str]:
        try:
            url = f"https://api.github.com/search/repositories?q={cve_id}"
            response = requests.get(url, headers=self.github_headers)
            response.raise_for_status()
            
            if response.status_code == 200:
                data = response.json()
                if "items" in data and len(data["items"]) > 0:
                    return [repo["html_url"] for repo in data["items"]]
            return []
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao buscar exploits no GitHub: {e}")
            return []

    def get_recent_cves(self) -> List[Dict]:
        try:
            start_date = datetime.now(UTC) - timedelta(days=1)
            params = {
                'pubStartDate': start_date.strftime("%Y-%m-%dT%H:%M:%S.000"),
                'pubEndDate': datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.000")
            }
            
            response = requests.get(self.nvd_api_url, params=params)
            response.raise_for_status()
            
            vulnerabilities = response.json().get('vulnerabilities', [])
            return vulnerabilities[:self.max_cves_per_day]
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao buscar CVEs: {e}")
            return []

    def format_cve_message(self, cve: Dict) -> str:
        cve_data = cve['cve']
        cve_id = cve_data['id']
        description = cve_data['descriptions'][0]['value']
        
        metrics = cve_data.get('metrics', {})
        cvss_v3 = metrics.get('cvssMetricV31', [{}])[0].get('cvssData', {})
        cvss_score = cvss_v3.get('baseScore', 'N/A')
        
        github_repos = self.search_github_exploits(cve_id)
        
        message = (
            f"🚨 Nova CVE Detectada 🚨\n\n"
            f"ID: {cve_id}\n"
            f"CVSS Score: {cvss_score}\n"
            f"Descrição: {description}\n"
            f"Link: https://nvd.nist.gov/vuln/detail/{cve_id}\n"
            f"📌 Exploits: {github_repos[0] if github_repos else 'Nenhum exploit encontrado'}"
        )

        return message

    def send_telegram_message(self, message: str) -> bool:
        try:
            payload = {
                'chat_id': self.chat_id,
                'message_thread_id': self.message_thread_id,
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
        self.logger.info("Iniciando monitor de CVEs...")
        while True:
            try:
                cves = self.get_recent_cves()
                for i, cve in enumerate(cves, 1):
                    message = self.format_cve_message(cve)
                    if self.send_telegram_message(message):
                        self.logger.info(f"Notificação {i}/{self.max_cves_per_day} enviada para CVE: {cve['cve']['id']}")
                    if i < len(cves):
                        time.sleep(self.message_delay)
                
                self.last_check_time = datetime.now(UTC)
                self.logger.info(f"Verificação concluída. Próxima verificação em {self.check_interval} segundos")
                time.sleep(self.check_interval)
                
            except Exception as e:
                self.logger.error(f"Erro inesperado: {e}")
                time.sleep(60)
