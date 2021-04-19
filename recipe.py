
class Recipe(object):
    '''
    TODO String
    '''
    def __init__(self, recipe=None, recipe_result=None):
        if recipe:
            self.recipe_id = recipe['recipe']['shareAs']
            self.recipe_name = recipe['recipe']['label']
            self.calories = recipe['recipe']['calories']
            self.time = recipe['recipe']['totalTime']
            self.cuisineType = recipe['recipe']['cuisineType']
            self.mealType = recipe['recipe']['mealType']
            self.dishType = recipe['recipe']['dishType']
            self.ingredient = recipe['recipe']['ingredientLines']
            self.healthLabels = recipe['recipe']['healthLabels']  
            self.totalNutrients = recipe['recipe']['totalNutrients']

        elif recipe_result:
            self.recipe_id = recipe_result['recipe_id']
            self.recipe_name = recipe_result['recipe_name']
            self.calories = recipe_result['calories']
            self.time = recipe_result['time']
            self.cuisineType = recipe_result['cuisineType']
            self.mealType = recipe_result['mealType']
            self.dishType = recipe_result['dishType']
            self.ingredient = recipe_result['ingredient']
            self.healthLabels = recipe_result['healthLabels']  
            self.totalNutrients = recipe_result['totalNutrients']
        else:
            self.recipe_id = 'no_id'
            self.recipe_name = 'no name'
            self.calories = 0.
            self.time = 0.
            self.cuisineType = []
            self.mealType = []
            self.dishType = []
            self.ingredient = []
            self.healthLabels = []
            self.totalNutrients = {}


    def __str__(self):
        '''
        TODO string
        '''
        return f'Recipe: {self.recipe_name}, Cuisine: {self.cuisineType}, '\
                f'Total Calories: {self.calories:.3f}'

    def to_json(self):
        '''
        TODO string
        '''
        return {'recipe_id': self.recipe_id, 
                'recipe_name': self.recipe_name,
                'calories': self.calories,
                'time': self.time,
                'cuisineType': self.cuisineType,
                'mealType': self.mealType,
                'dishType': self.dishType,
                'ingredient': self.ingredient,
                'healthLabels': self.healthLabels,
                'totalNutrients': self.totalNutrients}

