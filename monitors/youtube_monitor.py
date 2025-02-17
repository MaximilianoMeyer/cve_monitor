import requests
import logging
from typing import Optional, Tuple

class YouTubeMonitor:
    def __init__(self, api_key: str, channel_id: str, telegram_token: str, chat_id: str, message_thread_id: int):
        self.api_key = api_key
        self.channel_id = channel_id  # Apenas um canal por instância
        self.telegram_api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        self.chat_id = chat_id
        self.message_thread_id = message_thread_id
        self.logger = logging.getLogger(__name__)
        self.last_video_id = None  # Mantém controle do último vídeo enviado

    def get_latest_video(self) -> Optional[Tuple[str, str]]:
        """Obtém o vídeo mais recente do canal"""
        params = {
            'key': self.api_key,
            'channelId': self.channel_id,
            'part': 'snippet',
            'order': 'date',
            'maxResults': 1
        }

        try:
            response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
            response.raise_for_status()
            
            data = response.json()
            if "items" in data and data["items"]:
                video_id = data["items"][0]["id"].get("videoId")
                video_title = data["items"][0]["snippet"].get("title")
                
                if video_id and video_id != self.last_video_id:  
                    self.last_video_id = video_id  
                    return video_id, video_title  
            return None, None  

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao buscar vídeo do canal {self.channel_id}: {e}")
            return None, None  

    def send_telegram_message(self, message: str) -> bool:
        """Envia mensagem para o Telegram"""
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

    def check_and_notify(self):
        """Verifica e envia notificações para um canal"""
        video_id, video_title = self.get_latest_video()
        if video_id:
            message = (
                f"🎥 Novo vídeo disponível! 🎥\n\n"
                f"Título: {video_title}\n"
                f"Link: https://www.youtube.com/watch?v={video_id}"
            )
            if self.send_telegram_message(message):
                self.logger.info(f"Notificação enviada para o canal {self.channel_id}: {video_id}")
