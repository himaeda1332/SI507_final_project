# SI507_final_project
## 1. Libraries (not python standard library)
* [flask](https://flask.palletsprojects.com/en/1.1.x/): For making user interface
* [matplotlib](https://matplotlib.org): For making nutrients plot
* [pandas](https://pandas.pydata.org): For preprocessing to make nutrients plot
* [requests](https://docs.python-requests.org/en/master/): For fetching data through API
* [seaborn](https://seaborn.pydata.org): For making nutrients plot
* [google-api-python-client](https://github.com/googleapis/google-api-python-client): For using YouTube API  
### Installation
```shell
$ pip install flask matplotlib pandas requests seaborn
$ pip install google-api-python-client
```

## 2. API
In this application, we used two API.
### 1. EDAMAM
* [Edamam recipe search API](https://developer.edamam.com/admin)  
You can click the above link and need to sign up. Then, you can create your API key quickly.  
You can retrieve 2.3+ million nutritionally analyzed recipes.  

### 2. YouTube
* [YouTube Data API](https://developers.google.com/youtube/v3)  
To use this API, you need to create Google account at first, then you can create your API key on Google Cloud Platform.  
[This blog](https://blog.hubspot.com/website/how-to-get-youtube-api-key) is also helpful.  

## 3. How to use
You run the below code  
```shell
$ python main.py
```
1. User inputs keyword such as "beef tomato" and choose a cuisine type from the list such as "American" or "Japanese." Then, the app research recipes.  
2. The app returns the search results and shows the information of the meal, such as ingredients and calories. Also, the app shows the figure of how much nutrients the meal contains.  
3. When the user chooses a recipe which he/she wants to cook, the app searches related YouTube videos. User can choose a video and click it; then, it is shown on the new tab.  
4. Users can look for their search history.

