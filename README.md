## Table of Contents

- [Settings and Configurations](#settings-and-configurations)
  - [Logging Configuration](#logging-configuration)
  - [Database Configuration](#database-configuration)
- [Model Field Attributes](#model-field-attributes)
  - [auto_now_add](#auto_now_add)
  - [auto_now](#auto_now)
  - [Optional Fields](#optional-fields)
- [Migrations](#migrations)
  - [Creating an Empty Migration](#creating-an-empty-migration)
- [QuerySet Operations](#queryset-operations)
  - [Remove Nested from QuerySet](#remove-nested-from-queryset)
  - [Get Unique Values](#get-unique-values)
- [Model Management](#model-management)
  - [Get the Model](#get-the-model)
  - [Generate Inserts](#generate-inserts)
  - [Get Class Name](#get-class-name)
- [Django Admin Customization](#django-admin-customization)
  - [Display Fields](#display-fields)
  - [Filters](#filters)
  - [Search Fields](#search-fields)
  - [Organize Fields](#organize-fields)
- [Database Operations](#database-operations)
  - [Creating Objects](#creating-objects)
  - [Updating Objects](#updating-objects)
  - [Deleting Objects](#deleting-objects)
- [Choices and Enumerations](#choices-and-enumerations)
- [Bulk Operations](#bulk-operations)
  - [Bulk Update](#bulk-update)
  - [Bulk Creating Objects](#bulk-creating-objects)
- [Filtering and Excluding Data](#filtering-and-excluding-data)
- [Advanced Querying](#advanced-querying)
  - [Q Objects](#q-objects)
  - [F Objects](#f-objects)
  - [Annotate](#annotate)
  - [Prefetch Related](#prefetch-related)
  - [Raw Queries](#raw-queries)
- [Model Relations](#model-relations)
  - [ForeignKey (Many-to-One)](#foreignkey-many-to-one)
  - [ManyToManyField](#manytomanyfield)
  - [OneToOneField](#onetonefield)
- [Model Meta Options](#model-meta-options)
  - [Abstract Models](#abstract-models)
  - [Proxy Models](#proxy-models)
  - [Ordering and Indexing](#ordering-and-indexing)
- [Custom Fields and Validators](#custom-fields-and-validators)
  - [Custom Fields](#custom-fields)
  - [Validators](#validators)
- [Managers and Query Optimization](#managers-and-query-optimization)
  - [Custom Managers](#custom-managers)
- [Mixins](#mixins)
- [Data Validation and Saving](#data-validation-and-saving)

---

## Settings and Configurations

### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',  # Levels: CRITICAL, ERROR, WARNING, INFO, DEBUG
    },
    'loggers': {
        'django.db.backends': {  # SQL logs
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

Database Configuration

python

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "table_name",
        "USER": "postgres-user",
        "PASSWORD": "postgres-password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

Model Field Attributes
auto_now_add

    Description: Automatically sets the field to now when the object is first created.
    Behavior:
        When a new record (object) is created, the field is set to the current time of creation.
        Subsequent updates to the object won't change this field; it remains set to the initial creation time.

python

auto_now_add=True

auto_now

    Description: Automatically sets the field to now every time the object is saved.
    Behavior:
        When an object is created, the field is set to the current time.
        Every time the object is updated and saved, the field is updated to the current time.

python

auto_now=True

Optional Fields

    Parameters:
        null=True: Allows the database to store NULL for this field.
        blank=True: Allows the field to be blank in forms.

python

null=True
blank=True

Migrations
Creating an Empty Migration

To create an empty migration for custom operations:

bash

python manage.py makemigrations main_app --name migrate_unique_brands --empty

QuerySet Operations
Remove Nested from QuerySet

Retrieve a flat list of brand names without nesting:

python

print(Shoe.objects.values_list('brand', flat=True))

Get Unique Values

Retrieve a flat list of unique brand names:

python

print(Shoe.objects.values_list('brand', flat=True).distinct())

Model Management
Get the Model

Importing the Model:

python

from main_app.models import Shoe  # Not recommended in migration files

Using apps.get_model in Migrations:

python

shoe = apps.get_model('main_app', 'Shoe')

Generate Inserts

Using create:

python

for brand_name in ubn:
    unique_brands.create(brand_name=brand_name)  # Inserts one by one

Using bulk_create (More Optimal):

python

unique_brands.objects.bulk_create([
    unique_brands(brand_name=brand_name) for brand_name in ubn
])

Get Class Name

Retrieve the class name of a model:

python

Shoe.__name__

Django Admin Customization
Display Fields

Specify fields to display in the admin list view:

python

list_display = (
    'event_name',
    'participant_name',
    'registration_date'
)

Filters

Add filters to the admin sidebar:

python

list_filter = (
    'event_name',
    'registration_date'
)

Search Fields

Enable search functionality in the admin:

python

search_fields = (
    'event_name',
    'registration_date'
)

Organize Fields

Group fields into sections:

python

fieldsets = (
    ('Personal Information', {
        'fields': ('first_name', 'last_name', 'age', 'date_of_birth'),
    }),
    ('Academic Information', {
        'fields': ('grade',)
    }),
)

Template Example:

python

fieldsets = (({}), ({}))

Database Operations
Creating Objects

(Provide specific examples as needed)
Updating Objects

(Provide specific examples as needed)
Deleting Objects

Delete all employee records:

python

employees = Employee.objects.all()
employees.delete()

Choices and Enumerations

Example Model with Choices:

python

from django.db import models

class Department(models.Model):
    class Locations(models.TextChoices):
        SOFIA = "Sofia", 'Sofia'
        PLOVDIV = 'Plovdiv', 'Plovdiv'
        VARNA = 'Varna', 'Varna'
        BURGAS = 'Burgas', 'Burgas'
     
    location = models.CharField(
        max_length=20,
        choices=Locations.choices
    )

Bulk Operations
Bulk Update

Instead of saving each instance individually, use bulk_update for better performance.

Example Function:

python

from django.db.models import F

def increase_room_capacity() -> None:
    all_rooms = HotelRoom.objects.all().order_by('id')
    previous_room_capacity = None

    for room in all_rooms:
        if not room.is_reserved:
            continue
        if previous_room_capacity is not None:
            room.capacity += previous_room_capacity
        else:
            room.capacity += room.id

        previous_room_capacity = room.capacity
    HotelRoom.objects.bulk_update(all_rooms, ['capacity'])

Bulk Creating Objects

Example Function:

python

def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([
        first_art,
        second_art,
    ])

Filtering and Excluding Data
Filtering Data

Retrieve books based on genre and language:

python

books = Book.objects.filter(genre=genre, language=language)

Excluding Data

Exclude authors with no nationality:

python

authors = Author.objects.exclude(nationality=None)

Advanced Querying
Q Objects

Use Q objects for complex lookups with AND, OR, NOT, XOR operations.

Operators:

    AND: &
    OR: |
    NOT: ~
    XOR: ^

Example:

python

from django.db.models import Q

products = Product.objects.filter(
    Q(is_available=True) & Q(price__gt=3)
).order_by(
    '-price',
    'name'
)

Search Example:

python

@classmethod
def search_tasks(cls, query: str):
    return cls.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) 
    )

F Objects

Use F objects to refer to model fields directly in queries.

Example:

python

from django.db.models import F

product_to_be_discounted.update(price=F('price') * 0.7)

Another Example:

python

@classmethod
def ongoing_high_priority_task(cls):
    return cls.objects.filter(
        priority='High',
        is_completed=False,
        completion_date__gt=F('creation_date')
    )

Annotate

Add aggregate values to each item in the QuerySet.

Example:

python

from django.db.models import Sum, Count, Max

orders = Product.objects.annotate(
    total=Sum('orderproduct__quantity')
).values('name', 'total').order_by('-total')

Popular Locations Example:

python

def popular_locations(self) -> QuerySet:
    return self.values('location').annotate(
        location_count=Count('location')
    ).order_by('-location_count', 'location')[:2]

Highest Rated Game Example:

python

def highest_rated_game(self) -> QuerySet:
    return self.annotate(
        max_rating=Max('rating')
    ).order_by('-max_rating').first()

Prefetch Related

Optimize queries involving related objects.

Example:

python

orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

Another Example:

python

def get_programmers_with_technologies(self) -> QuerySet:
    return self.programmers.prefetch_related('projects__technologies_used')

Raw Queries

Execute raw SQL queries.

Example:

python

employees = Employee.objects.raw('SELECT * FROM users_employee')

Model Relations
ForeignKey (Many-to-One)

Example:

python

class Department(models.Model):
    # Department fields...

class Employee(models.Model):
    # Employee fields...
    department = models.ForeignKey(
        to=Department,
        on_delete=models.CASCADE, 
        related_name='employees'
    )

On Delete Options:

python

class Employee(models.Model):
    # Employee fields...
    manager = models.ForeignKey(
        to=Manager,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True
    )
    department = models.ForeignKey(
        to=Department,
        on_delete=models.RESTRICT
    )

ManyToManyField

Example with Through Model:

python

class StudentEnrollment(models.Model):
    student = models.ForeignKey(
        to='Student',
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        to='Course',
        on_delete=models.CASCADE
    )
    enrollment_date = models.DateField()

Another Example:

python

class Employee(models.Model):
    # Employee fields...

class Project(models.Model):
    # Project fields...
    employees = models.ManyToManyField(
        Employee, 
        through='ProjectAssignment'
    )

class ProjectAssignment(models.Model):
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )
    project = models.ForeignKey(
        Project, 
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    role = models.CharField(max_length=30)

OneToOneField

Example:

python

class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(
        Lecturer,
        on_delete=models.CASCADE
    )
    # Additional fields...

Model Meta Options
Abstract Models

Abstract models are not created as database tables and are used as base classes.

python

class Meta:
    abstract = True

Proxy Models

Proxy models share the same database table as their parent model but can have different behavior.

python

class Meta:
    proxy = True

Ordering and Indexing

Ordering:

python

class Meta:
    ordering = ['-rating']
    verbose_name = 'Restaurant Review'
    verbose_name_plural = 'Restaurant Reviews'
    unique_together = ['reviewer_name', 'restaurant']

Indexing:

python

from django.db import models

class Meta:
    indexes = [
        models.Index(fields=['menu'], name='main_app_menu_review_menu_id')
    ]

Custom Fields and Validators
Custom Fields

BooleanChoiceField Example:

python

from django.db import models

class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ((True, 'Available'), (False, 'Not Available'))
        kwargs['default'] = True
        super().__init__(*args, **kwargs)

StudentIDField Example:

python

from django.db import models
from django.core.exceptions import ValidationError

class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValidationError('Invalid input for student ID')

    def get_prep_value(self, value):
        clean_value = self.to_python(value)

        if clean_value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')
        return clean_value

Validators

Example with CharField:

python

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, message='Name must be at least 2 characters long.'),
            MaxLengthValidator(100, message='Name cannot exceed 100 characters.')
        ]
    )

Common Validators:

    MinValueValidator
    MaxValueValidator
    RegexValidator
    EmailValidator
    URLValidator
    validate_ipv4_address
    validate_ipv6_address
    validate_ipv46_address
    validate_comma_separated_integer_list
    int_list_validator
    DecimalValidator
    FileExtensionValidator

Email Field Example:

python

from django.db import models

email = models.EmailField(
    error_messages={
        'invalid': 'Enter a valid email address'
    }
)

Custom Validator Example:

python

from django.core.exceptions import ValidationError

def validate_menu_categories(value):
    required_categories = ["Appetizers", "Main Course", "Desserts"]
    missing_categories = [category for category in required_categories if category not in value]

    if missing_categories:
        raise ValidationError(
            'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".'
        )

Validator Class Example:

python

from django.core.exceptions import ValidationError

class RangeValueValidator:
    def __init__(self, min_value: int, max_value: int, message=None):
        self.min_value = min_value
        self.max_value = max_value
        if not message:
            self.message = f"The rating must be between {self.min_value:.1f} and {self.max_value:.1f}"
        else:
            self.message = message

    def __call__(self, value: int):
        if not self.min_value <= value <= self.max_value:
            raise ValidationError(self.message)

    def deconstruct(self):
        return (
            'main_app.validator.RangeValueValidator',
            [self.min_value, self.max_value],
            {'message': self.message}
        )

Managers and Query Optimization
Custom Managers

Example Manager:

python

from django.db import models

class ProductManager(models.Manager):
    def available_products(self):
        return self.filter(is_available=True)
    
    def available_products_in_category(self, category_name: str):
        return self.filter(category__name=category_name, is_available=True)

Assigning the Manager to a Model:

python

class Product(models.Model):
    # Product fields...
    
    objects = ProductManager()

Mixins

Example Mixin:

python

class RechargeEnergyMixin:
    def recharge_energy(self, amount: int) -> None:
        self.energy = min(100, self.energy + amount)
        self.save()

class Hero(models.Model, RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()

Data Validation and Saving
Saving an Instance to the Database

python

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

Data Validation Before Saving

Using clean and full_clean:

python

from django.core.exceptions import ValidationError

def clean(self):
    if self.specialty not in self.Specialization.choices:
        raise ValidationError('Specialty must be a valid choice.')

def save(self, *args, **kwargs):
    self.full_clean()
    super().save(*args, **kwargs)

Creating and Managing Objects in the Database
Adding an Object to a Many-to-Many Relationship

python

def add_song_to_artist(artist_name: str, song_title: str):
    artist_object = Artist.objects.get(name=artist_name)
    song_object = Song.objects.get(title=song_title)
    artist_object.songs.add(song_object)

Removing an Object from a Many-to-Many Relationship

python

def remove_song_from_artist(artist_name: str, song_title: str):
    artist_object = Artist.objects.get(name=artist_name)
    song_object = Song.objects.get(title=song_title)
    artist_object.songs.remove(song_object)

Example Functions
Calculate Average Rating for a Product

python

def calculate_average_rating_for_product_by_name(product_name: str):
    product_object = Product.objects.get(name=product_name)
    reviews_for_product = product_object.reviews.all()
    total_rating = sum(r.rating for r in reviews_for_product)
    avg_rating = total_rating / len(reviews_for_product)

    return avg_rating

Get All Products with No Reviews

python

def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')

Additional Tips

    Do Not Import Models in Migration Files: Use apps.get_model instead.
    Use bulk_create and bulk_update for Performance: These methods are more efficient for large datasets.
    Leverage Django Admin for Better Management: Customize list displays, filters, and search fields to enhance the admin interface.
    Implement Validators and Custom Fields: Ensure data integrity and enforce business rules at the model level.
    Optimize Queries with select_related and prefetch_related: Reduce the number of database hits for related objects.
