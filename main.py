import requests
import pprint
import json
from googleapiclient.discovery import build

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

# From user's imput
params = {"q":"beef", 
            "cuisineType": "Japanese"}


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
    request_key = construct_unique_key(params)
    if request_key in CACHE_DICT.keys():
        print("fetching cached data")
        return CACHE_DICT[request_key]
    else:
        print("making new request")
        CACHE_DICT[request_key] = make_request(params)
        save_cache(CACHE_DICT)
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

def make_youtube_request_with_cache(keyword):
    '''Check the cache for a saved result for this params:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    Parameters
    ----------
    keyword: string
        Keyword for query
    Returns
    -------
    list
        the results of the query as a list loaded from cache
        JSON
    '''
    params = {'keyword': keyword}
    request_key = construct_unique_key(params)
    if request_key in CACHE_YOUTUBE_DICT.keys():
        print("fetching cached data")
        return CACHE_YOUTUBE_DICT[request_key]
    else:
        print("making new request")
        CACHE_YOUTUBE_DICT[request_key] = get_youtube_data(keyword)
        save_cache(CACHE_YOUTUBE_DICT)
        return CACHE_YOUTUBE_DICT[request_key]


def main():

    response = make_request_with_cache(params)
    for i, recipe in enumerate(response):
        print(i, Recipe(recipe_result=recipe))
    print()

    youtube_results = make_youtube_request_with_cache('Baked Chicken')
    for i, youtube in enumerate(youtube_results):
        print(i, Video(result=youtube))
    print()
    save_cache(CACHE_DICT, source='recipe')
    save_cache(CACHE_YOUTUBE_DICT, source='youtube')


if __name__ == '__main__':

    CACHE_DICT = load_cache(source='recipe')
    CACHE_YOUTUBE_DICT = load_cache(source='youtube')
    main()
