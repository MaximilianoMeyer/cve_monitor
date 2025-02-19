# utils/config.py
import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    
    config = {
        'telegram_token': os.getenv('TELEGRAM_TOKEN'),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'message_thread_id': os.getenv('TELEGRAM_MESSAGE_THREAD_ID', "0"),
	'TELEGRAM_YOUTUBE_THREAD_ID': os.getenv('TELEGRAM_YOUTUBE_THREAD_ID', "0"),
        'github_token': os.getenv('GITHUB_TOKEN'),
        'youtube_api_key': os.getenv('YOUTUBE_API_KEY'),
        "youtube_channel_ids": [ch.strip() for ch in os.getenv("YOUTUBE_CHANNEL_IDS", "").split(",") if ch.strip()],  # Lista de canais limpa
        'check_interval': int(os.getenv('CHECK_INTERVAL', '300')),  # Tempo padrão: 5 min
        'message_delay': int(os.getenv('MESSAGE_DELAY', '2'))
    }
    
    required = ['telegram_token', 'chat_id', 'message_thread_id', 'TELEGRAM_YOUTUBE_THREAD_ID']
    missing = [key for key in required if not config[key]]
    
    if missing:
        raise ValueError(f"Variáveis de ambiente obrigatórias não definidas: {', '.join(missing)}")
    
    return config
