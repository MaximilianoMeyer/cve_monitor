# monitors/youtube_monitor.py
import requests
import logging
from typing import Optional
from datetime import datetime, UTC

class YouTubeMonitor:
    def __init__(self, api_key: str, channel_id: str, telegram_token: str, chat_id: str, message_thread_id: int):
        self.api_key = api_key
        self.channel_id = channel_id
        self.last_video_id = None
        self.base_url = "https://www.googleapis.com/youtube/v3/search"
        self.telegram_api_url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
        self.chat_id = chat_id
        self.message_thread_id = message_thread_id
        self.logger = logging.getLogger(__name__)

    def get_latest_video(self) -> Optional[tuple]:
        params = {
            'key': self.api_key,
            'channelId': self.channel_id,
            'part': 'snippet',
            'order': 'date',
            'maxResults': 1
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if "items" in data and len(data["items"]) > 0:
                video_id = data["items"][0]["id"].get("videoId")
                video_title = data["items"][0]["snippet"].get("title")
                if video_id and video_id != self.last_video_id:
                    self.last_video_id = video_id
                    return video_id, video_title
            return None, None
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Erro ao buscar vídeo do YouTube: {e}")
            return None, None

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

    def check_and_notify(self):
        video_id, video_title = self.get_latest_video()
        if video_id:
            message = (
                f"🎥 Novo vídeo disponível! 🎥\n\n"
                f"Título: {video_title}\n"
                f"Link: https://www.youtube.com/watch?v={video_id}"
            )
            if self.send_telegram_message(message):
                self.logger.info(f"Notificação de novo vídeo enviada: {video_id}")