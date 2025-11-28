# Quiz & Event App

This is a Django-based Quiz + Event application.  
It allows:

- Viewing and taking quizzes  
- Administering quizzes (via simple dashboard)  
- Displaying upcoming events  

## Requirements

- Python 3.x  
- Django 4.x (or latest)  
- A virtual environment (recommended)  

## Setup Instructions

1. Create and activate virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux / macOS
# source venv/bin/activate

2. Install dependencies
pip install django

3. Apply migrations
python manage.py makemigrations
python manage.py migrate

4. Load sample data (fixtures)
python manage.py loaddata sample_data.json

5. Run the development server
python manage.py runserver

6. Open in browser
Home: http://127.0.0.1:8000/
Quizzes list: http://127.0.0.1:8000/quizzes/
Events list: http://127.0.0.1:8000/events/
Dashboard (to add quizzes / questions): http://127.0.0.1:8000/dashboard/
