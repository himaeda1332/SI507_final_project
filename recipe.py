class Recipe(object):
    '''a recipe object, which has the information about the recipe
    This instance can be made from several type
    Class Attributes
    ----------------
    recipe_id: string
        the recipe id: unique
    url: string
        the url of the recipe to opne in browser
    recipe_name: string
        the recipe is unique
    calories: float
        total calories of the meal
    time: float
        time for cooking the meal
    cuisineType: string
        the cuisine type
    servings: float
        the number of servings
    ingredient: list
        ingredients, each attributes is each ingredient
    totalDaily: dict
        the parcentage of daily nutrient
    file_name: string
        the file name to open thumbnail image
    '''
    def __init__(self, recipe=None, recipe_result=None):
        if recipe:
            self.recipe_id = recipe['recipe']['uri']
            self.url = recipe['recipe']['shareAs']
            self.recipe_name = recipe['recipe']['label']
            self.calories = round(recipe['recipe']['calories'], 3)
            self.time = recipe['recipe']['totalTime']
            self.cuisineType = recipe['recipe']['cuisineType'][0]
            self.servings = recipe['recipe']['yield'] + 1
            self.ingredient = recipe['recipe']['ingredientLines']
            self.totalDaily = recipe['recipe']['totalDaily']
            self.image = recipe['recipe']['image']
            self.file_name = self.recipe_id[self.recipe_id.find("#")+1:]

        elif recipe_result:
            self.recipe_id = recipe_result['recipe_id']
            self.url = recipe_result['url']
            self.recipe_name = recipe_result['recipe_name']
            self.calories = recipe_result['calories']
            self.time = recipe_result['time']
            self.cuisineType = recipe_result['cuisineType']
            self.servings = recipe_result['servings']
            self.ingredient = recipe_result['ingredient']
            self.totalDaily = recipe_result['totalDaily']
            self.image = recipe_result['image']
            self.file_name = recipe_result['file_name']

        else:
            self.recipe_id = 'no_id'
            self.url = 'no url'
            self.recipe_name = 'no name'
            self.calories = 0.
            self.time = 0.
            self.cuisineType = 'no label'
            self.servings = 1.0
            self.ingredient = []
            self.totalDaily = {}
            self.image = 'no image'
            self.file_name = 'no name'


    def to_json(self):
        '''convert the object to python dictionary object
        Parameters
        ----------
        None
        Returns
        -------
        dict
        '''
        return {'recipe_id': self.recipe_id,
                'recipe_name': self.recipe_name,
                'calories': self.calories,
                'time': self.time,
                'cuisineType': self.cuisineType,
                'servings': self.servings,
                'ingredient': self.ingredient,
                'totalDaily': self.totalDaily,
                'image': self.image,
                'url': self.url,
                'file_name': self.file_name}

