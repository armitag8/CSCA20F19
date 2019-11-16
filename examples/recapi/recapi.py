import requests
import random

type_of_recipe = input("What kind of recipe you want to see? ")

response = requests.get("http://www.recipepuppy.com/api/?q=" + type_of_recipe)

recipes = response.json()['results']

print(recipes[random.randint(0, len(recipes) - 1)])
