from googleapiclient.discovery import build
import os
import json


class Channel:
    """Класс для ютуб-канала"""
    YT_API_KEY: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.title = self.channel_info().get('snippet').get('title')
        self.description = self.channel_info().get('snippet').get('description')
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = self.channel_info().get('statistics').get('subscriberCount')
        self.video_count = self.channel_info().get('statistics').get('videoCount')
        self.view_count = self.channel_info().get('statistics').get('viewCount')

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def channel_info(self) -> dict:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        return channel.get('items')[0]

    @classmethod
    def get_service(cls):
        return cls.youtube

    def to_json(self, name):
        with open(name, mode='a', encoding='utf8') as file:
            out_data = json.dumps(self.__dict__)
            file.write(out_data)

    def __str__(self):
        return f'{self.title}({self.url})'

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return int(self.subscriber_count) - int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)


if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    # print(moscowpython.__dict__)
    # moscowpython.to_json('moscowpython.json')

    # получаем значения атрибутов
    # print(moscowpython.title)  # MoscowPython
    # print(moscowpython.video_count)  # 685 (может уже больше)
    # print(moscowpython.url)  # https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A
    # moscowpython.channel_id = 'Новое название'
    highload = Channel('UCwHL6WHUarjGfUM_586me8w')

    # Используем различные магические методы
    print(moscowpython)  # 'MoscowPython (https://www.youtube.com/channel/UC-OVMPlMA3-YCIeg4z5z23A)'
    print(moscowpython + highload)  # 100100
    print(moscowpython - highload)  # -48300
    print(highload - moscowpython)  # 48300
    print(moscowpython > highload)  # False
    print(moscowpython >= highload)  # False
    print(moscowpython < highload)  # True
    print(moscowpython <= highload)  # True
