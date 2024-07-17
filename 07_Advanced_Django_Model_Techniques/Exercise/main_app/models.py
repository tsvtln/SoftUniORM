from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, URLValidator, MinLengthValidator
from django.db import models as m

md = m.Model


# Mixins
class RechargeEnergyMixin:
    def recharge_energy(self, amount: int) -> None:
        self.energy = min(100, self.energy + amount)
        self.save()


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


### TAX-INDUCING PRICING ###
class Product(md):
    name = m.CharField(
        max_length=100,
    )

    price = m.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def calculate_tax(self) -> Decimal:
        return self.price * Decimal(0.08)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal) -> Decimal:
        return Decimal(weight * 2)

    def format_product_name(self) -> str:
        return f'Product: {self.name}'


class DiscountedProduct(Product):
    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> Decimal:
        return self.price * Decimal(1.20)

    def calculate_tax(self) -> Decimal:
        return self.price * Decimal(0.05)

    @staticmethod
    def calculate_shipping_cost(weight: Decimal) -> Decimal:
        return weight * Decimal(1.50)

    def format_product_name(self):
        return f'Discounted Product: {self.name}'


### SUPERHERO UNIVERSE ###
class Hero(md, RechargeEnergyMixin):
    name = m.CharField(
        max_length=100,
    )
    hero_title = m.CharField(
        max_length=100,
    )
    energy = m.PositiveIntegerField()


class SpiderHero(Hero):
    class Meta:
        proxy = True

    def swing_from_buildings(self) -> str:
        if self.energy - 80 >= 0:
            self.energy -= 80 if self.energy - 80 > 0 else 79  # max(1, self.energy - 80)
            self.save()
            return f"{self.name} as Spider Hero swings from buildings using web shooters"

        return f"{self.name} as Spider Hero is out of web shooter fluid"


class FlashHero(Hero):
    class Meta:
        proxy = True

    def run_at_super_speed(self) -> str:
        if self.energy - 65 >= 0:
            self.energy -= 65 if self.energy - 65 > 0 else 64
            self.save()
            return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

        return f"{self.name} as Flash Hero needs to recharge the speed force"