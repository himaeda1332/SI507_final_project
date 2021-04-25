import json
import requests

from googleapiclient.discovery import build
import sqlite3
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

import secrets
from recipe import Recipe
from youtube import Video
import utils

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)

@app.route('/', methods=["GET", "POST"])
def start_app():
    if request.method == 'GET':
        utils.save2sqlite()
    return render_template('index.html')


@app.route('/recipes', methods=["POST"])
def show_recipes():
    keywords = request.form.get('keywords')
    cuisineType = request.form.get('cuisineType')
    params = {"q": keywords,
            "cuisineType": cuisineType}
    recipe_results = utils.make_request_with_cache(params)
    return render_template('recipes.html', recipe_results=recipe_results,
                            size=len(recipe_results),
                            keywords=keywords, cuisineType=cuisineType)


@app.route('/video', methods=["POST"])
def show_youtube_videos():
    recipe_no = request.form.get('recipe_no')
    recipe_name = request.form.get(f'recipe_name_{recipe_no}')
    recipe_id = request.form.get(f'recipe_id_{recipe_no}')
    keywords = request.form.get('keywords')
    cuisineType = request.form.get('cuisineType')
    youtube_results = utils.make_youtube_request_with_cache(recipe_name,
                                                            recipe_id)
    utils.save2sqlite()
    return render_template('video.html', youtube_results=youtube_results,
                            recipe_id=recipe_id,
                            recipe_name=recipe_name,
                            keywords=keywords, cuisineType=cuisineType)


@app.route('/history', methods=["GET", "POST"])
def show_recipe_history():
    history_results = utils.make_history()
    return render_template('history.html',
                                history_results=history_results,
                                size=len(history_results))


@app.route('/video_hist', methods=["POST"])
def show_video_history():
    recipe_no = request.form.get('recipe_no')
    recipe_name = request.form.get(f'recipe_name_{recipe_no}')
    recipe_id = request.form.get(f'recipe_id_{recipe_no}')
    keywords = request.form.get('keywords')
    cuisineType = request.form.get('cuisineType')
    youtube_results = utils.make_youtube_request_with_cache(recipe_name,
                                                            recipe_id)
    return render_template('video_hist.html',
                            youtube_results=youtube_results,
                            recipe_id=recipe_id,
                            recipe_name=recipe_name,
                            keywords=keywords, cuisineType=cuisineType)

if __name__ == '__main__':

    app.run(debug=True)
