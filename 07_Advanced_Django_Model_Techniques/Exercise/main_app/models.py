from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator, MinLengthValidator
from django.db import models as m

md = m.Model


# Custom Validators
def letter_space_check(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError('Name can only contain letters and spaces')


def age_check(value):
    if value < 18:
        raise ValidationError('Age must be greater than or equal to 18')


def phone_check(value):
    if value[:4] != '+359' or len(value) != 13:
        raise ValidationError("Phone number must start with '+359' followed by 9 digits")


# Create your models here.
class Customer(md):
    name = m.CharField(
        max_length=100,
        validators=[letter_space_check]
    )

    age = m.PositiveIntegerField(
        validators=[age_check]
    )

    email = m.EmailField(
        error_messages={
            'invalid': 'Enter a valid email address'
        }
    )

    phone_number = m.CharField(
        max_length=13,
        validators=[phone_check]
    )

    website_url = m.URLField(
        error_messages={
            'invalid': 'Enter a valid URL'
        }
    )


### MEDIA ###
class BaseMedia(md):
    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']

    title = m.CharField(
        max_length=100
    )

    description = m.TextField()

    genre = m.CharField(
        max_length=50
    )
    created_at = m.DateField(
        auto_now_add=True
    )


class Book(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'

    author = m.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(5, message='Author must be at least 5 characters long')
        ]
    )

    isbn = m.CharField(
        max_length=20,
        unique=True,
        validators=[
            MinLengthValidator(6, message='ISBN must be at least 6 characters long')
        ]
    )


class Movie(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'

    director = m.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(8, message='Director must be at least 8 characters long')
        ]
    )


class Music(BaseMedia):
    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'

    artist = m.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(9, message='Artist must be at least 9 characters long')
        ]
    )

