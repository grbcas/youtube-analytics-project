import datetime
import os
import isodate
from datetime import timedelta
from googleapiclient.discovery import build

YT_API_KEY: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=YT_API_KEY)


class PlayList:
	def __init__(self, playlist_id):
		self.playlist_id = playlist_id
		self.title = self.playlist_info()['items'][0]['snippet']['localized']['title']
		self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
		self.playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
		                                                    part='contentDetails',
		                                                    maxResults=50,
		                                                    ).execute()
		self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
		self.video_response = youtube.videos().list(part='contentDetails,statistics',
		                                            id=','.join(self.video_ids)
		                                            ).execute()

	def playlist_info(self):
		playlist_videos = youtube.playlists().list(part='snippet',
		                                           id=self.playlist_id,
		                                           ).execute()
		return playlist_videos

	@property
	def total_duration(self):
		res = timedelta()

		for video in self.video_response['items']:
			# YouTube video duration is in ISO 8601 format
			iso_8601_duration = video['contentDetails']['duration']
			duration = isodate.parse_duration(iso_8601_duration)
			res += duration
		return res

	def show_best_video(self):
		likes = 0
		best_video_url = ''

		for video_id in self.video_ids:
			video_request = youtube.videos().list(
				part='statistics',
				id=video_id
			).execute()

			like_count = video_request['items'][0]['statistics']['likeCount']

			if int(like_count) > likes:
				likes = int(like_count)
				best_video_url = f"https://youtu.be/{video_request['items'][0]['id']}"

		return best_video_url


if __name__ == '__main__':
	pl = PlayList('PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw')
	assert pl.title == "Moscow Python Meetup №81"
	assert pl.url == "https://www.youtube.com/playlist?list=PLv_zOGKKxVpj-n2qLkEM2Hj96LO6uqgQw"
	# print(pl.__dict__)

	duration = pl.total_duration
	print(duration)
	assert str(duration) == "1:49:52"
	assert isinstance(duration, datetime.timedelta)
	assert duration.total_seconds() == 6592.0
	print(pl.show_best_video())
