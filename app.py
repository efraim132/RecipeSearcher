from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import User, load_recipes, add_recipe, remove_recipe
from forms import DietaryForm, LoginForm, RecipeForm, SignupForm, RemoveRecipeForm
from dashboard import log_activity, start_dashboard
import os
import sys

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
        log_activity(f"User searched for recipes with requirements: {', '.join(selected_requirements)}")
    
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
            log_activity(f"User logged in: {form.username.data}")
            return redirect(url_for('index'))
        flash('Invalid username or password')
        log_activity(f"Failed login attempt for user: {form.username.data}")
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
            log_activity(f"New user registered: {form.username.data}")
            return redirect(url_for('login'))
        else:
            flash('Username already exists.')
            log_activity(f"Failed registration attempt - username exists: {form.username.data}")
    return render_template('signup.html', form=form)

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    log_activity(f"User logged out: {username}")
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
        log_activity(f"User {current_user.username} added new recipe: {form.name.data}")
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
            log_activity(f"User {current_user.username} removed recipe: {recipe_name}")
        else:
            flash('Recipe not found.')
            log_activity(f"Failed recipe removal attempt by {current_user.username}: {recipe_name}")
        return redirect(url_for('index'))
    return render_template('remove_recipe.html', form=form)

# Main block to run the application
if __name__ == '__main__':
    # Create an admin user if it doesn't exist
    if not User.get('admin'):
        User.create('admin', 'admin123')  # Change this password in production!
        log_activity("Admin user created")
    
    # Start the dashboard in a separate thread
    try:
        start_dashboard()
    except Exception as e:
        print(f"Warning: Could not start dashboard: {str(e)}")
        print("The application will continue without the dashboard.")
    
    # Run the Flask application
    app.run(debug=True)