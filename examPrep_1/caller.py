import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# dummy data
# from main_app.models import Director, Actor, Movie
# from dummy_data import populate_model_with_data
# populate_model_with_data(Movie, 20)

# Import your models here

# Create queries within functions
