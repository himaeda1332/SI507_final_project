import requests
import json
from googleapiclient.discovery import build
import sqlite3
import hashlib

import secrets
from recipe import Recipe
from youtube import Video
import utils

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


def main():

    recipe_results = utils.make_request_with_cache(params)
    for i, recipe in enumerate(recipe_results):
        print(i, Recipe(recipe_result=recipe))
    print()

    # From user's input
    recipe_id = "1http://www.edamam.com/recipe/soy-glazed-beef-bdb68821a6bc806469bd17f34ca382b9/beef"
    recipe_name = "Miso Beef Noodle Soup"

    youtube_results = utils.make_youtube_request_with_cache(recipe_name, recipe_id)
    for i, youtube in enumerate(youtube_results):
        print(i, Video(result=youtube))
    print()
    
    # utils.save2sqlite(recipe_results, recipe_id, youtube_results)


if __name__ == '__main__':

    CACHE_DICT = utils.load_cache(source='recipe')
    CACHE_YOUTUBE_DICT = utils.load_cache(source='youtube')

    main()

    utils.save_cache(CACHE_DICT, source='recipe')
    utils.save_cache(CACHE_YOUTUBE_DICT, source='youtube')
