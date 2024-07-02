import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Shoe

# print(Shoe.objects.values_list('brand_name', flat=True).distinct())
