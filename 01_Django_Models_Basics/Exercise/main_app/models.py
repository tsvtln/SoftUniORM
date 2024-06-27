from django.db import models as m


class Person(m.Model):
    name = m.CharField(
        max_length=30,
    )

    age = m.PositiveIntegerField()


class Blog(m.Model):
    post = m.TextField()
    author = m.CharField(
        max_length=35,
    )


class WeatherForecast(m.Model):
    date = m.DateField()
    temperature = m.FloatField()
    humidity = m.FloatField()
    precipitation = m.FloatField()


class Recipe(m.Model):
    name = m.CharField(
        max_length=100,
        unique=True,
    )
    description = m.TextField()
    ingredients = m.TextField()
    cook_time = m.PositiveIntegerField()
    created_at = m.DateTimeField(
        auto_now_add=True,
    )


class Product(m.Model):
    name = m.CharField(
        max_length=70,
    )
    description = m.TextField()
    price = m.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    created_at = m.DateTimeField(
        auto_now_add=True,
    )


class UserProfile(m.Model):
    username = m.CharField(
        max_length=65,
        unique=True,
    )
    first_name = m.CharField(
        max_length=40,
    )
    last_name = m.CharField(
        max_length=40,
    )
    email = m.EmailField(
        unique=True,
        default='students@softuni.bg',
    )
    bio = m.TextField(
        max_length=120,
    )
    profile_image_url = m.URLField()
    created_at = m.DateTimeField(
        auto_now_add=True,
    )


class Exercise(m.Model):
    name = m.CharField(
        max_length=100,
    )
    description = m.TextField()
    difficulty_level = m.CharField(
        max_length=20,
    )
    duration_minutes = m.PositiveIntegerField()
    equipment = m.CharField(
        max_length=90,
    )
    video_url = m.URLField(
        null=True,
        blank=True,
    )
    calories_burned = m.PositiveIntegerField(
        default=1,
    )
    is_favorite = m.BooleanField(
        default=False,
    )
