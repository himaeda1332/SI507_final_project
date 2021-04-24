class Recipe(object):
    '''
    TODO String
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
        '''
        TODO string
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

