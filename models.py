import pickle
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

RECIPES_FILE = 'recipes.pkl' # File to store recipes
USERS_FILE = 'users.pkl' # File to store users TODO: move this to a database



class User(UserMixin):
    """
    A class representing a user.
    Attributes:
        username (str): The username of the user.
        password_hash (str): The hashed password of the user.
        id (str): The ID of the user, which is the same as the username.
    Methods:
        get(user_id):
            Retrieves a user by their ID.
        create(username, password):
            Creates a new user with the given username and password.
        check_password(password):
            Checks if the provided password matches the stored hashed password.
    """

    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.id = username  # Using username as the ID

    @staticmethod
    def get(user_id):
        users = load_users()
        return users.get(user_id)

    @staticmethod
    def create(username, password):
        users = load_users()
        if username in users:
            return False
        users[username] = User(username, generate_password_hash(password))
        save_users(users)
        return True

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def load_recipes():
    """
    Load recipes from a file if it exists, otherwise return a default list of recipes.
    This function checks if a file specified by the global variable RECIPES_FILE exists.
    If the file exists, it loads and returns the recipes from the file using the pickle module.
    If the file does not exist, it returns a default list of recipes.
    Returns:
        list: A list of recipe dictionaries, each containing the following keys:
            - 'name' (str): The name of the recipe.
            - 'dietary_requirements' (list): A list of dietary requirement tags (e.g., 'high_protein', 'low_carb').
            - 'calories' (int): The number of calories in the recipe.
            - 'protein' (int): The amount of protein in grams.
            - 'description' (str): A brief description of the recipe.
    """

    if os.path.exists(RECIPES_FILE):
        with open(RECIPES_FILE, 'rb') as f:
            return pickle.load(f)
    return [
        {
            'name': 'High-Protein Chicken Bowl',
            'dietary_requirements': ['high_protein', 'low_carb'],
            'calories': 450,
            'protein': 40,
            'description': 'Grilled chicken breast with quinoa and roasted vegetables'
        },
        {
            'name': 'Vegan Buddha Bowl',
            'dietary_requirements': ['vegan', 'low_calorie'],
            'calories': 350,
            'protein': 15,
            'description': 'Chickpeas, sweet potato, kale, and tahini dressing'
        },
        {
            'name': 'Keto Steak Salad',
            'dietary_requirements': ['keto', 'high_protein'],
            'calories': 500,
            'protein': 35,
            'description': 'Grilled steak with avocado and mixed greens'
        }
    ]

def save_recipes(recipes):
    with open(RECIPES_FILE, 'wb') as f:
        pickle.dump(recipes, f)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'wb') as f:
        pickle.dump(users, f)

def add_recipe(recipe):
    recipes = load_recipes()
    recipes.append(recipe)
    save_recipes(recipes)
    return True

def remove_recipe(recipe_name):
    """
    Removes a recipe by its name from the list of recipes.
    Args:
        recipe_name (str): The name of the recipe to be removed.
    Returns:
        bool: True if the recipe was found and removed, False if the recipe was not found.
    """

    recipes = load_recipes()
    updated_recipes = [recipe for recipe in recipes if recipe['name'] != recipe_name]
    if len(updated_recipes) == len(recipes):
        return False  # Recipe not found
    save_recipes(updated_recipes)
    return True