from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField, PasswordField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, EqualTo

# Form for selecting dietary requirements
class DietaryForm(FlaskForm):
    dietary_requirements = SelectMultipleField('Dietary Requirements', choices=[
        ('high_protein', 'High Protein'),
        ('low_carb', 'Low Carb'),
        ('keto', 'Keto'),
        ('vegan', 'Vegan'),
        ('low_calorie', 'Low Calorie')
    ])
    submit = SubmitField('Find Recipes')

# Form for user login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Form for user signup
class SignupForm(FlaskForm):
    """
    SignupForm class for user registration.

    Fields:
        username (StringField): Field for entering the username. It is required.
        password (PasswordField): Field for entering the password. It is required.
        confirm_password (PasswordField): Field for confirming the password. It is required and must match the password field.
        submit (SubmitField): Field for submitting the form.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


# Form for adding a new recipe
class RecipeForm(FlaskForm):
    """
    RecipeForm is a FlaskForm for creating and validating recipe entries.
    Fields:
        name (StringField): The name of the recipe. This field is required.
        description (TextAreaField): A description of the recipe. This field is required.
        calories (IntegerField): The number of calories in the recipe. This field is required and must be a non-negative integer.
        protein (IntegerField): The amount of protein in grams in the recipe. This field is required and must be a non-negative integer.
        dietary_requirements (SelectMultipleField): A list of dietary requirements that the recipe meets. The choices include 'High Protein', 'Low Carb', 'Keto', 'Vegan', and 'Low Calorie'.
        submit (SubmitField): A submit button to add the recipe.
    """

    name = StringField('Recipe Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    calories = IntegerField('Calories', validators=[DataRequired(), NumberRange(min=0)])
    protein = IntegerField('Protein (g)', validators=[DataRequired(), NumberRange(min=0)])
    dietary_requirements = SelectMultipleField('Dietary Requirements', choices=[
        ('high_protein', 'High Protein'),
        ('low_carb', 'Low Carb'),
        ('keto', 'Keto'),
        ('vegan', 'Vegan'),
        ('low_calorie', 'Low Calorie')
    ])
    submit = SubmitField('Add Recipe')

# Form for removing a recipe
class RemoveRecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name', validators=[DataRequired()])
    submit = SubmitField('Remove Recipe')