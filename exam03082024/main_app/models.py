from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator
from django.db import models

from main_app.model_manager import AstronautManager

# Validators
digits_only = RegexValidator(
    regex=r'^\d+$',
    message='This field must contain only digits.',
    code='invalid_digits'
)


# Create your models here.

class Astronaut(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[digits_only],
    )

    is_active = models.BooleanField(
        default=True,
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    spacewalks = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    # def __str__(self):
    #     return self.name

    objects = AstronautManager()


class Spacecraft(models.Model):
    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )

    manufacturer = models.CharField(
        max_length=100,
    )

    capacity = models.SmallIntegerField(
        validators=[MinValueValidator(1)],
    )

    weight = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )

    launch_date = models.DateField()

    updated_at = models.DateTimeField(
        auto_now=True,
    )
    #
    # def __str__(self):
    #     return self.name


class Mission(models.Model):
    class Statuses(models.TextChoices):
        PLANNED = 'Planned', 'Planned'
        ONGOING = 'Ongoing', 'Ongoing'
        COMPLETED = 'Completed', 'Completed'

    name = models.CharField(
        max_length=120,
        validators=[MinLengthValidator(2)],
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        choices=Statuses.choices,
        max_length=9,
        default=Statuses.PLANNED,
    )

    launch_date = models.DateField()

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    spacecraft = models.ForeignKey(
        to='Spacecraft',
        on_delete=models.CASCADE,
    )

    astronauts = models.ManyToManyField(
        to='Astronaut',
        related_name='missions',
    )

    commander = models.ForeignKey(
        to='Astronaut',
        on_delete=models.SET_NULL,
        null=True,
    )

    # def __str__(self):
    #     return self.name
