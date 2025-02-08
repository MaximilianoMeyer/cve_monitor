# utils/config.py
import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    
    config = {
        'telegram_token': os.getenv('TELEGRAM_TOKEN'),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID'),
        'message_thread_id': int(os.getenv('TELEGRAM_MESSAGE_THREAD_ID')),
        'github_token': os.getenv('GITHUB_TOKEN'),
        'youtube_api_key': os.getenv('YOUTUBE_API_KEY'),
        'youtube_channel_id': os.getenv('YOUTUBE_CHANNEL_ID'),
        'check_interval': int(os.getenv('CHECK_INTERVAL', '3600')),
        'message_delay': int(os.getenv('MESSAGE_DELAY', '2'))
    }
    
    required = ['telegram_token', 'chat_id', 'message_thread_id']
    missing = [key for key in required if not config[key]]
    
    if missing:
        raise ValueError(f"Variáveis de ambiente obrigatórias não definidas: {', '.join(missing)}")
    
    return config