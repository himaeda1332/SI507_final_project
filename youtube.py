from googleapiclient.discovery import build
import secrets

API_YOUTUBE_KEY = secrets.YOUTUBE_API_KEY
youtube = build('youtube', 'v3', developerKey=API_YOUTUBE_KEY)

class Video(object):
    '''
    TODO String
    '''
    def __init__(self, json=None, result=None):
        if json:
            self.video_id = json['id']['videoId']
            self.channel_title = json['snippet']['channelTitle']
            self.published = json['snippet']['publishedAt']
            self.channel_id = json['snippet']['channelId']
            self.title = json['snippet']['title']
            self.description = json['snippet']['description']
        elif result:
            self.video_id = result['video_id']
            self.channel_title = result['channel_title']
            self.published = result['published']
            self.channel_id = result['channel_id']
            self.title = result['title']
            self.description = result['description']
            self.viewCount = result['viewCount']
            self.likeCount = result['likeCount']
            self.dislikeCount = result['dislikeCount']
            self.commentCount = result['commentCount']
        else:
            self.video_id = 'no_id'
            self.channel_title = 'no title'
            self.published = 'no_date'
            self.channel_id = 'no_id'
            self.title = 'no title'
            self.description = 'None'


    def get_statistics(self):
        '''
        TODO string
        '''
        statistics = youtube.videos().list(part = 'statistics', 
                        id = self.video_id).\
                            execute()['items'][0]['statistics']
        self.viewCount = statistics['viewCount']
        self.likeCount = statistics['likeCount']
        self.dislikeCount = statistics['dislikeCount']
        self.commentCount = statistics['commentCount']
        
    def to_json(self):
        '''
        TODO string
        '''
        return {'video_id': self.video_id, 
                'title': self.title,
                'published': self.published,
                'channel_id': self.channel_id,
                'channel_title': self.channel_title,
                'description': self.description,
                'viewCount': self.viewCount,
                'likeCount': self.likeCount,
                'dislikeCount': self.dislikeCount,
                'commentCount': self.commentCount}

    def __str__(self):
        '''
        TODO string
        '''
        return f'Title: {self.title}\n Description: {self.description}\n '\
                f'View count: {self.viewCount}\n Like count: {self.likeCount}\n'



