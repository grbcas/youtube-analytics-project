from googleapiclient.discovery import build
import os
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = Channel.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    yt = Channel.api_key
    print(yt)
    yt_id = 'UC-OVMPlMA3-YCIeg4z5z23A'
    moscowpython = Channel(yt_id)
    moscowpython.print_info()
