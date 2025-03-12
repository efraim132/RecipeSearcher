from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, load_recipes, add_recipe, remove_recipe
from forms import DietaryForm, LoginForm, RecipeForm, SignupForm, RemoveRecipeForm  # Import forms from forms.py
import os

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Route for the home page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = DietaryForm()
    matching_recipes = []
    
    if form.validate_on_submit():
        selected_requirements = form.dietary_requirements.data
        recipes = load_recipes()
        matching_recipes = [
            recipe for recipe in recipes
            if any(req in recipe['dietary_requirements'] for req in selected_requirements)
        ]
    
    return render_template('index.html', form=form, recipes=matching_recipes)

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)

# Route for user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = SignupForm()
    if form.validate_on_submit():
        if User.create(form.username.data, form.password.data):
            flash('Account created successfully! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
    return render_template('signup.html', form=form)

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Route for adding a new recipe
@app.route('/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe_route():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = {
            'name': form.name.data,
            'description': form.description.data,
            'calories': form.calories.data,
            'protein': form.protein.data,
            'dietary_requirements': form.dietary_requirements.data
        }
        add_recipe(recipe)
        flash('Recipe added successfully!')
        return redirect(url_for('index'))
    return render_template('add_recipe.html', form=form)

# Route for removing a recipe
@app.route('/remove_recipe', methods=['GET', 'POST'])
@login_required
def remove_recipe_route():
    form = RemoveRecipeForm()
    if form.validate_on_submit():
        recipe_name = form.recipe_name.data
        if remove_recipe(recipe_name):
            flash('Recipe removed successfully!')
        else:
            flash('Recipe not found.')
        return redirect(url_for('index'))
    return render_template('remove_recipe.html', form=form)

# Main block to run the application
if __name__ == '__main__':
    # Create an admin user if it doesn't exist
    if not User.get('admin'):
        User.create('admin', 'admin123')  # Change this password in production!
    app.run(debug=True)