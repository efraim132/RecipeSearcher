# Fitness Recipe Finder

Fitness Recipe Finder is a web application that helps users find recipes based on their dietary requirements. Users can sign up, log in, add new recipes, and remove existing recipes.

## Features

- User authentication (sign up, log in, log out)
- Add new recipes
- Remove existing recipes
- Search for recipes based on dietary requirements

## Technologies Used

- Flask
- Flask-WTF
- Flask-Login
- WTForms
- Bootstrap 5

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd CursorTest
    ```

2. **Create a virtual environment (optional but recommended):**

    ```sh
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```env
    SECRET_KEY=your-secret-key-here
    ```

5. **Run the application:**

    ```sh
    python app.py
    ```

6. **Access the application:**

    Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

### Home Page

- The home page allows users to search for recipes based on dietary requirements.
- Users can select multiple dietary requirements and click "Find Recipes" to see matching recipes.

### User Authentication

- **Sign Up:** Users can create a new account by providing a username and password.
- **Log In:** Existing users can log in with their username and password.
- **Log Out:** Logged-in users can log out.

### Adding a Recipe

- Logged-in users can add new recipes by providing the recipe name, description, calories, protein, and dietary requirements.

### Removing a Recipe

- Logged-in users can remove existing recipes by providing the recipe name.

## Project Structure

- `app.py`: Main application file containing routes and application setup.
- `models.py`: Contains the `User` class and functions for loading, saving, adding, and removing recipes.
- `forms.py`: Contains WTForms classes for various forms used in the application.
- `templates/`: Contains HTML templates for different pages.
- `static/css/style.css`: Custom CSS for styling the application.
- `requirements.txt`: List of required Python packages.

## License

This project is licensed under the MIT License.