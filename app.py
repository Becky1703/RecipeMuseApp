from flask import Flask, render_template, request
import requests
from urllib.parse import unquote

#Creates flask app
app = Flask(__name__)

#My Spoonacular API Key
API_KEY = "5a3a0133ba904a66b9e3a9fa055e52aa"

#Defines route for the home page
@app.route('/home', methods=['GET'])
def home():
    #renders the home page with empty recipe list
    return render_template('home.html', recipes=[], search_query="")

#Defines the main route for the app
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        #Gets the search query from the form
        query = request.form.get('search_query', '')
        #Gets the recipes from the Spoonacular API
        recipes = get_recipes(query)
        #Renders the home page with the recipes
        return render_template('home.html', recipes=recipes, search_query=query)
     
     #if the request method is GET or no form was submitted
    search_query = request.args.get('search_query', '')
    decoded_search_query = unquote(search_query)

    #Perform a search for recipes with the search query
    recipes = get_recipes(decoded_search_query)

    #Renders the home page with the recipes
    return render_template('home.html', recipes=recipes, search_query=decoded_search_query)

#Function to get recipes from the Spoonacular API
def get_recipes(query):     
    #Sends a GET request to the Spoonacular API
    url = f"https://api.spoonacular.com/recipes/complexSearch"
    params = {
        'apiKey': API_KEY,
        'query': query,
        'number': '10',
        'instructionsRequired': 'True',
        'addRecipeInformation': 'True',
        'fillIngredients': 'True'
    }
    #Sends the request and returns the response
    response = requests.get(url, params=params)

    #If the API call doesnt return an Error
    if response.status_code == 200:
        #Parse the API response as data
        data = response.json()
        #Return list of recipes
        return data['results']
    #if the API call returns an Error
    return []

#Route to view a specific recipe with a given recipe ID
@app.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe(recipe_id):
    #Gets search query from the form
    search_query = request.args.get('search_query', '')

    #Build url using the specific recipe ID
    url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    params = {
        'apiKey': API_KEY,
    }

    #Send GET request to the Spoonacular API to get the recipe information
    response = requests.get(url, params=params)

    #If the API call doesnt return an Error
    if response.status_code == 200:
        #Parse the API response as data
        recipe = response.json()
        return render_template('view_recipe.html', recipe=recipe, search_query=search_query)
    return "Recipe not found", 404

#Runs the app in debug mode when executed
if __name__ == '__main__':
    app.run('0.0.0.0, port=5006', debug=True)
