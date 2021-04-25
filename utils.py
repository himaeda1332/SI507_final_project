import requests
import json
import sqlite3
import datetime

from googleapiclient.discovery import build
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

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
    according to the source
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    source: string
        Source name (e.c. recipe or youtube)

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

    search_url = BASE_URL + "?q=" + params["q"] +\
            "&app_id=" + API_ID + "&app_key=" + API_KEY +\
                f"&cuisineType={params['cuisineType']}"
    response = requests.get(search_url).json()
    cache_list = []
    for recipe_json in response['hits']:
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
        the results of the recipes as JSON format
    '''
    CACHE_DICT = load_cache(source='recipe')
    request_key = construct_unique_key(params)
    if request_key in CACHE_DICT.keys():
        print("fetching cached data")
        return CACHE_DICT[request_key]
    else:
        print("making new request")
        response = make_request(params)
        create_plot(response)
        CACHE_DICT[request_key] = response
        save_cache(CACHE_DICT, source='recipe')
        return CACHE_DICT[request_key]


def create_plot(response):
    '''Create plot to show top 5 nutrients rate of each cuisine
    required per day.
    This function uses list of recipe objects, then it creates
    plot by using recipe's file name attribute.

    Parameters
    ----------
    response: list
        List of Recipe objects
    Returns
    -------
    None
    '''
    for recipe in response:
        label = []
        weight = []
        servings = recipe['servings']
        i = 0
        for daily in recipe['totalDaily'].values():
            label.append(daily['label'])
            weight.append(daily['quantity'] / servings)
            i += 1
            if i == 5:
                break
        img_name = recipe['file_name']
        plt.figure(figsize=(4, 3))
        temp = pd.DataFrame(data={'label': label,
                                'weight': weight})
        sns.barplot(x='label', y='weight', data=temp)
        plt.xlabel("Nutrient")
        plt.ylabel("Daily")
        plt.ylim((0, 100))
        plt.ioff()
        plt.savefig(f"./static/figures/{img_name}.png")


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
        recipe id used for request_key
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
        keyword_token = keyword.split()
        keyword = " ".join(keyword_token[:4])
        print("making new request")
        CACHE_YOUTUBE_DICT[request_key] = get_youtube_data(keyword)
        save_cache(CACHE_YOUTUBE_DICT, source='youtube')
        return CACHE_YOUTUBE_DICT[request_key]


def save2sqlite():
    '''Create database about recipe and youtube vidoes which
    user searched before.
    The recipe information is splited into 3 tables called recipes,
    ingredients and nutrients.
    The youtube information is recorded in a table, which has recipe_id
    as a foreign key.
    Parameters
    ----------
    None
    Returns
    -------
    None
    '''
    CACHE_DICT = load_cache(source='recipe')
    CACHE_YOUTUBE_DICT = load_cache(source='youtube')

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    create_table_recipes = '''
        create table if not exists "recipes" (
            "request_key"   text    not null,
            "recipe_id"     text    unique,
            "recipe_name"   text    not null,
            "url"           text    not null,
            "calories"      real    not null,
            "servings"      real    not null,
            "cuisinetype"   text    not null,
            "image"         text    not null,
            "file_name"     text    not null,
            primary key(request_key, recipe_id)
        );
    '''

    create_table_ingredients = '''
        create table if not exists "ingredients" (
            "recipe_id"     text    not null,
            "ingredient_id" integer not null,
            "ingredient"   text    not null,
            foreign key(recipe_id) references recipes(recipe_id),
            primary key(recipe_id, ingredient_id)
        );
    '''

    create_table_nutrients = '''
        create table if not exists "nutrients" (
            "recipe_id"     text    not null,
            "nutrient_id" integer not null,
            "nutrient"   text    not null,
            "quantity"   real    not null,
            foreign key(recipe_id) references recipes(recipe_id),
            primary key(recipe_id, nutrient_id)
        );
    '''

    create_table_youtube = '''
        create table if not exists "youtube" (
            "video_id"        text    primary key,
            "title"           text    not null,
            "published"       text    not null,
            "viewcount"       integer not null,
            "likecount"       integer not null,
            "dislikecount"    integer not null,
            "commentcount"    integer not null,
            "image"           text    not null,
            "url"             text    not null,
            "recipe_id"       text    not null,
            "daytime"         text    not null,
            foreign key(recipe_id) references recipes(recipe_id)
        );
    '''
    cur.execute(create_table_recipes)
    cur.execute(create_table_ingredients)
    cur.execute(create_table_nutrients)
    cur.execute(create_table_youtube)

    for key, recipe_dict in CACHE_DICT.items():
        for recipe in recipe_dict:
            insert_into_recipe = f'''
                insert into recipes values('{key}',
                '{recipe['recipe_id']}',
                "{recipe['recipe_name']}", "{recipe['url']}",
                {recipe['calories']}, {recipe['servings']},
                '{recipe['cuisineType']}', '{recipe['image']}',
                '{recipe['file_name']}')
            '''
            try:
                cur.execute(insert_into_recipe)
            except sqlite3.IntegrityError:
                pass
            for i, ingredient in enumerate(recipe['ingredient']):

                insert_into_ingredient = f'''
                    insert into ingredients values('{recipe['recipe_id']}',
                    {i}, "{ingredient}"")
                '''
                try:
                    cur.execute(insert_into_ingredient)
                except sqlite3.IntegrityError:
                    pass

        for i, nutrient in enumerate(recipe['totalDaily'].values()):
            insert_into_nutrient = f'''
                insert into nutrients values('{recipe['recipe_id']}', {i},
                "{nutrient['label']}", {nutrient['quantity']})
            '''
            try:
                cur.execute(insert_into_nutrient)
            except sqlite3.IntegrityError:
                pass

    for key, youtube_dict in CACHE_YOUTUBE_DICT.items():
        for youtube in youtube_dict:
            insert_into_youtube = f'''
                insert into youtube values('{youtube['video_id']}',
                "{youtube['title']}", '{youtube['published']}',
                {youtube['viewCount']}, {youtube['likeCount']},
                {youtube['dislikeCount']}, {youtube['commentCount']},
                '{youtube['image']}', '{youtube['url']}',
                '{key[10:]}', "{str(datetime.datetime.today())}")
            '''
            try:
                cur.execute(insert_into_youtube)
            except sqlite3.IntegrityError:
                    pass

    conn.commit()
    cur.close()
    conn.close()


def make_history():
    '''Retrieve last 10 recipe information from database.
    recipe_id in the youtube table is used as a key, then
    retrieve at most 10 recipe information from the database.
    Parameters
    ----------
    None
    Returns
    -------
    list:
        the results of the recipes as JSON format
    '''
    recipe_history = []
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    query = '''
            SELECT distinct recipe_id from
                    (select recipe_id, daytime
                        from youtube order by daytime desc)
                    limit 10
            '''
    result = cur.execute(query).fetchall()
    for fetch_id in result:
        recipe_id = fetch_id[0]
        query_recipe = f'''
            SELECT * from recipes
                where recipe_id = "{recipe_id}"
            '''
        recipe = cur.execute(query_recipe).fetchall()
        temp_recipe = Recipe()
        temp_recipe.recipe_id = recipe[0][1]
        temp_recipe.recipe_name = recipe[0][2]
        temp_recipe.url = recipe[0][3]
        temp_recipe.calories = recipe[0][4]
        temp_recipe.servings = recipe[0][5]
        temp_recipe.cuisineType = recipe[0][6]
        temp_recipe.image = recipe[0][7]
        temp_recipe.file_name = recipe[0][8]

        query_ingredient = f'''
            SELECT * from ingredients
                where recipe_id = "{recipe_id}"
            '''
        ingredients = cur.execute(query_ingredient).fetchall()
        ingredient_list = []
        for ingredient in ingredients:
            ingredient_list.append(ingredient[2])
        temp_recipe.ingredient = ingredient_list
        query_nutrients = f'''
            SELECT * from nutrients
                where recipe_id = "{recipe_id}"
            '''
        nutrients = cur.execute(query_nutrients).fetchall()
        nutrient_dict = {}
        for i, nutrient in enumerate(nutrients):
            nutrient_dict[str(i)] = {"label": nutrient[2],
                                        "quantity": nutrient[3],
                                        "unit": "%"}
        temp_recipe.totalDaily = nutrient_dict
        recipe_history.append(temp_recipe.to_json())

    return recipe_history

