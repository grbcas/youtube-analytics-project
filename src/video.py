from googleapiclient.discovery import build
import os

YT_API_KEY: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=YT_API_KEY)


class Video:
	"""
	получить статистику видео по его id
	"""

	def __init__(self, video_id):
		self.video_id = video_id
		video_response = self.video()
		try:
			self.title: str = video_response['items'][0]['snippet']['title']
			self.view_count: int = video_response['items'][0]['statistics']['viewCount']
			self.like_count: int = video_response['items'][0]['statistics']['likeCount']
			self.comment_count: int = video_response['items'][0]['statistics']['commentCount']
		except IndexError:
			self.title = None
			self.view_count = None
			self.like_count = None
			self.comment_count = None

	def __str__(self):
		return f'{self.title}'

	def video(self):
		"""
		получить статистику видео по его id
		"""
		video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
		                                       id=self.video_id).execute()
		return video_response


class PLVideo(Video):
	"""
	Получить данные по видеороликам в плейлисте
	"""

	def __init__(self, video_id, playlist_id):
		super().__init__(video_id)
		self.playlist_id = playlist_id

	def playlist(self):
		"""
		Получить данные по видеороликам в плейлисте
		"""
		playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
		                                               part='contentDetails',
		                                               maxResults=50,
		                                               ).execute()
		return playlist_videos

	def __str__(self):
		return f'{self.title}'


if __name__ == '__main__':
	video1 = Video('AWX4JnAnjBE')  # 'AWX4JnAnjBE' - это id видео из ютуб
	video2 = PLVideo('4fObz_qw9u4', 'PLv_zOGKKxVph_8g2Mqc3LMhj0M_BfasbC')
	print(video1)
	assert str(video1) == 'GIL в Python: зачем он нужен и как с этим жить'
	print(video2)
	assert str(video2) == 'MoscowPython Meetup 78 - вступление'
