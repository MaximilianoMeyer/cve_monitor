import time
import logging
from threading import Thread
from monitors.cve_monitor import CVEMonitor
from monitors.youtube_monitor import YouTubeMonitor
from utils.config import load_config
from utils.logger import setup_logging

def run_youtube_monitor(monitor):
    while True:
        try:
            monitor.check_and_notify()
            time.sleep(300)  # Define um tempo de espera entre verificações
        except Exception as e:
            logging.error(f"Erro no monitor do YouTube: {e}")
            time.sleep(60)

def main():
    # Configura o logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Carrega as configurações
    try:
        config = load_config()
    except ValueError as e:
        logger.error(f"Erro ao carregar configurações: {e}")
        return

    # Solicita input do usuário para quantidade de CVEs
    try:
        max_cves = int(input("Digite a quantidade de CVEs que deseja receber: "))
    except ValueError:
        logger.error("Valor inválido para quantidade de CVEs")
        return

    # Inicia o monitor de CVEs
    cve_monitor = CVEMonitor(
        config['telegram_token'],
        config['chat_id'],
        config['message_thread_id'],
        github_token=config['github_token'],
        max_cves_per_day=max_cves,
        check_interval=config['check_interval'],
        message_delay=config['message_delay']
    )

    # Inicia as threads
    Thread(target=cve_monitor.run).start()

    # Criar monitores para múltiplos canais do YouTube
    youtube_api_key = config["youtube_api_key"]
    telegram_token = config["telegram_token"]
    chat_id = config["chat_id"]
    message_thread_id = int(config["message_thread_id"])  # Certifica-se de que é int

    for channel_id in config["youtube_channel_ids"]:
        channel_id = channel_id.strip()  # Remove espaços extras
        if channel_id:  # Evita IDs vazios
            youtube_monitor = YouTubeMonitor(
                youtube_api_key, channel_id, telegram_token, chat_id, message_thread_id
            )
            Thread(target=run_youtube_monitor, args=(youtube_monitor,)).start()

if __name__ == "__main__":
    main()
