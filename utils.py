import requests
import json
from googleapiclient.discovery import build
import sqlite3

import secrets
from recipe import Recipe
from youtube import Video

API_ID = secrets.RECIPE_API_ID
API_KEY = secrets.RECIPE_API_KEY
API_YOUTUBE_KEY = secrets.YOUTUBE_API_KEY

BASE_URL = "https://api.edamam.com/search"

CACHE_FILE_NAME = 'cache.json'
CACHE_DICT = {}

CACHE_YOUTUBE_FILE_NAME = 'cache_youtube.json'
CACHE_YOUTUBE_DICT = {}

DB_NAME = "Recipe.sqlite"


def load_cache(source='recipe'):
    ''' opens the cache file if it exists and loads the JSON into
    a dictionary, which it then returns.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None

    Returns
    -------
    The opened cache
    '''
    if source == 'recipe':
        file_name = CACHE_FILE_NAME
    else:
        file_name = CACHE_YOUTUBE_FILE_NAME
    try:
        cache_file = open(file_name, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache, source='recipe'):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    if source == 'recipe':
        file_name = CACHE_FILE_NAME
    else:
        file_name = CACHE_YOUTUBE_FILE_NAME

    cache_file = open(file_name, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def construct_unique_key(params):
    ''' constructs a key that is guaranteed to uniquely and
    repeatably identify an API request by its baseurl and params

    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs

    Returns
    -------
    string
        the unique key as a string
    '''
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = connector.join(param_strings)
    return unique_key


def make_request(params):
    '''Make a request to the Web API using the baseurl and params

    Parameters
    ----------
    params: dict
        A dictionary of param:value pairs

    Returns
    -------
    list
        the data returned from making the request in the form of
        a list
    '''

    search_url = BASE_URL + "?q=" + params["q"] + "&app_id=" + API_ID + "&app_key=" + API_KEY
    if params['cuisineType']:
        search_url += f"&cuisineType={params['cuisineType']}"
    response = requests.get(search_url).json()
    cache_list = []
    for i, recipe_json in enumerate(response['hits']):
        recipe = Recipe(recipe_json)
        cache_list.append(recipe.to_json())

    return cache_list


def make_request_with_cache(params):
    '''Check the cache for a saved result for this params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    Parameters
    ----------
    params: dict
        Paramters for query
    Returns
    -------
    list
        the results of the query as a list loaded from cache
        JSON
    '''
    CACHE_DICT = load_cache(source='recipe')

    request_key = construct_unique_key(params)
    if request_key in CACHE_DICT.keys():
        print("fetching cached data")
        return CACHE_DICT[request_key]
    else:
        print("making new request")
        CACHE_DICT[request_key] = make_request(params)
        save_cache(CACHE_DICT, source='recipe')
        return CACHE_DICT[request_key]


def get_youtube_data(keyword):
    '''Make a request to the Web API using the baseurl and params

    Parameters
    ----------
    keyword: string
        A keyword to search on YouTube

    Returns
    -------
    list
        the data returned from making the request in the form of
        a list
    '''
    cache_list = []
    youtube = build('youtube', 'v3', developerKey=API_YOUTUBE_KEY)
    output = youtube.search().list(
        part='snippet',
        q=keyword,
        order='viewCount',
        type='video',
        maxResults=10
    ).execute()

    for result in output['items']:
        video = Video(result)
        video.get_statistics()
        cache_list.append(video.to_json())

    return cache_list


def make_youtube_request_with_cache(keyword, recipe_id):
    '''Check the cache for a saved result for this params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    Parameters
    ----------
    keyword: string
        Keyword for query
    recipe_id: string
        Keyword for query
    Returns
    -------
    list
        the results of the query as a list loaded from cache
        JSON
    '''
    CACHE_YOUTUBE_DICT = load_cache(source='youtube')

    params = {'recipe_id': recipe_id}
    request_key = construct_unique_key(params)
    if request_key in CACHE_YOUTUBE_DICT.keys():
        print("fetching cached data")
        return CACHE_YOUTUBE_DICT[request_key]
    else:
        print("making new request")
        CACHE_YOUTUBE_DICT[request_key] = get_youtube_data(keyword)
        save_cache(CACHE_YOUTUBE_DICT, source='youtube')
        return CACHE_YOUTUBE_DICT[request_key]

def save2sqlite(recipe_data=None, recipe_id=None, youtube_data=None):
    '''
    TODO string
    '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    create_table_recipes = '''
        create table if not exists "recipes" (
            "recipe_id"     text    primary key,
            "recipe_name"   text    not null,
            "calories"      real    not null   
        );
    '''
    create_table_youtube = '''
        create table if not exists "youtube" (
            "video_id"        text    primary key,
            "title"           text    not null,
            "published"       text    not null,
            "description"     text,
            "viewcount"       integer not null,
            "likecount"       integer not null,
            "dislikecount"    integer not null,
            "commentcount"    integer not null,
            "recipe_id"       text    not null,
            foreign key(recipe_id) references recipes(recipe_id)
        );
    '''
    cur.execute(create_table_recipes)
    cur.execute(create_table_youtube)

    for recipe in recipe_data:
        insert_into_recipe = f'''
            insert into recipes values({recipe['recipe_id']}, 
            {recipe['recipe_name']}, {recipe['calories']})
        '''
        cur.execute(insert_into_recipe)
    
    for youtube in youtube_data:
        insert_into_youtube = f'''
            insert into youtube values({youtube['video_id']},
            {youtube['title']}, {youtube['published']},
            {youtube['description']}, {youtube['viewCount']},
            {youtube['likeCount']}, {youtube['dislikeCount']},
            {youtube['commentCount']}, {recipe_id})
        '''
        cur.execute(insert_into_youtube)
    
    conn.commit()
    cur.close()
    conn.close()
