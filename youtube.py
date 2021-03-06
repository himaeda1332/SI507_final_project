from googleapiclient.discovery import build
import secrets

API_YOUTUBE_KEY = secrets.YOUTUBE_API_KEY
youtube = build('youtube', 'v3', developerKey=API_YOUTUBE_KEY)

class Video(object):
    '''a youtube video object
    This instance can be made from several type
    Class Attributes
    ----------------
    video_id: string
        the video id: unique
    channel_title: string
        the channel title which the video is included
    published: string
        published date
    channel_id: string
        the channel id
    viewCount: integer
        the number of viewing
    likeCount: integer
        the number of like
    dislikeCount: integer
        the number of dislike
    commentCount: integer
        the number of comments
    image: string
        the thumbnail file name
    url: string
        the video url to open in the browser
    '''
    def __init__(self, json=None, result=None):
        if json:
            self.video_id = json['id']['videoId']
            self.channel_title = json['snippet']['channelTitle']
            self.published = json['snippet']['publishedAt']
            self.channel_id = json['snippet']['channelId']
            self.title = json['snippet']['title']
            self.image = json['snippet']['thumbnails']['default']['url']
            self.url = "https://www.youtube.com/watch?v=" + self.video_id

        elif result:
            self.video_id = result['video_id']
            self.channel_title = result['channel_title']
            self.published = result['published']
            self.channel_id = result['channel_id']
            self.title = result['title']
            self.viewCount = result['viewCount']
            self.likeCount = result['likeCount']
            self.dislikeCount = result['dislikeCount']
            self.commentCount = result['commentCount']
            self.image = result['image']
            self.url = result['url']

        else:
            self.video_id = 'no_id'
            self.channel_title = 'no title'
            self.published = 'no_date'
            self.channel_id = 'no_id'
            self.title = 'no title'
            self.image = 'no image'


    def get_statistics(self):
        '''the funcction to get statistics from video id
        Parameters
        ----------
        None
        Returns
        -------
        None
        '''
        statistics = youtube.videos().list(part = 'statistics',
                        id = self.video_id).\
                            execute()['items'][0]['statistics']
        try:
            self.viewCount = statistics['viewCount']
        except KeyError:
            self.viewCount = 0
        try:
            self.likeCount = statistics['likeCount']
        except KeyError:
            self.likeCount = 0
        try:
            self.dislikeCount = statistics['dislikeCount']
        except KeyError:
            self.dislikeCount = 0
        try:
            self.commentCount = statistics['commentCount']
        except KeyError:
            self.commentCount = 0


    def to_json(self):
        '''convert the object to python dictionary object
        Parameters
        ----------
        None
        Returns
        -------
        dict
        '''
        return {'video_id': self.video_id,
                'title': self.title,
                'published': self.published,
                'channel_id': self.channel_id,
                'channel_title': self.channel_title,
                'viewCount': self.viewCount,
                'likeCount': self.likeCount,
                'dislikeCount': self.dislikeCount,
                'commentCount': self.commentCount,
                'image': self.image,
                'url': self.url}

