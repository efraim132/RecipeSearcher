import pickle
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

RECIPES_FILE = 'recipes.pkl'
USERS_FILE = 'users.pkl'

class User(UserMixin):
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