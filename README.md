settings and configs:
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
        'level': 'DEBUG',  # Other levels CRITICAL, ERROR, WARNING, INFO, DEBUG
    },
    'loggers': {
        'django.db.backends': {  # responsible for the sql logs
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

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

auto adds:
auto_now_add= True 
• When a new record (object) is created, the field is set to the current time of creation.
• Subsequent updates to the object won't change this field; it remains set to the initial creation time.

auto_now = True # 
• When an object is created, the field is set to the current time.
• Every time the object is updated and saved, the field is updated to the current time.

optional field:
null=True,
blank=True

Empty migration:
makemigrations main_app --name migrate_unique_brands --empty

Remove nested from query set:
print(Shoe.objects.values_list('brand', flat=True))
--- flat=True 

Get unique values from the query set list:
print(Shoe.objects.values_list('brand', flat=True).distinct())

-- .distinct()


Get the model:
from main_app.models import Shoe  (not to be done in migrations files)
for model apps: 
shoe = apps.get_model('main_app', 'Shoe')

Generate inserts:
for brand_name in ubn:
    unique_brands.create(brand_name=brand_name)  # insert into unique_brands(brand_name) values (brand_name)
    
unique_brands.objects.bulk_create([unique_brands(brand_name=brand_name) for brand_name in ubn])  # more optimal way 


Get class name:
Shoe.__name__


django admin fields (display fields):
list_display = (
    'event_name',
    'participant_name',
    'registration_date'
)


django admin filters:
list_filter = (
    'event_name',
    'registration_date'
)


django admin search fields:
search_fields = (
    'event_name',
    'registration_date'
)


organize fields:
fieldsets = (
    ('Personal Information', {
        'fields': ('first_name', 'last_name', 'age', 'date_of_birth'),
    }),

    ('Academic Information', {
        'fields': ('grade',)
    }),
)

template: fieldsets = (({}), ({}))


creating objects in the DB:




updating objects in the DB:



deleting objects in the DB:
employees = Employee.objects.all()
employees.delete()


choices:
class Department(models.Model):
    class Locations(models.TextChoices):
        SOFIA = "Sofia", 'Sofia'
        PLOVDIV = 'Plovdiv', 'Plovdiv'
        VARNA = 'Varna', 'Varna'
        BURGAS = 'Burgas', 'Burgas'
     
     location = models.CharField(
        max_length=20,
        choices=Locations
    )
    

bulk update:
instead of room.save()
HotelRoom.objects.bulk_update(all_rooms, ['capacity'])

eg:
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
        # room.save()
    HotelRoom.objects.bulk_update(all_rooms, ['capacity'])
    
    
update something specific:
ChessPlayer.objects.filter(title="GM").update(games_won=30)

update choices:
Laptop.objects.filter(brand='Asus').update(operation_system=Laptop.OperatingSystems.WINDOWS)




filtering data:
books = Book.objects.filter(genre=genre, language=language)



excluding data:
authors = Author.objects.exclude(nationality=None)


get by id (or something else):
review = Review.objects.get(id=1)


Matching the exact value of the field (case-sensitive by default):
    Employee.objects.filter(job_level="Jr.")
    Employee.objects.exclude(job_level__exact="Jr.")  # explicit form
    Employee.objects.get(email_address__iexact="a@b.com")  # case-insensitive match
    
Matching values that contain a specific substring
Employee.objects.exclude(job_title__contains="Engineer")
Employee.objects.filter(job_title__icontains="engineer") # case-insensitive


Matching values starting with or ending with a given string
Employee.objects.exclude(job_level__startswith="Sr.")
Employee.objects.filter(job_title__endswith="Engineer")


Matching field values greater than a given value
Employee.objects.filter(id__gt=2) # greater than
Employee.objects.exclude(id__gte=2) # greater than or equal to


Matching field values less than a given value
Employee.objects.filter(id__lt=5) # less than
Employee.objects.exclude(id__lte=5) # less than or equal to


Matching field values in a range (inclusive)
Employee.objects.filter(id__range=(2, 5)) # from 2 to 5, both inclusive

def in_price_range(self, min_price: Decimal, max_price: Decimal) -> QuerySet:
    return self.filter(price__range=[min_price, max_price])





bulk creating objects:
def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([
        first_art,
        second_art,
    ])


add object to db:
def add_song_to_artist(artist_name: str, song_title: str):
    artist_object = Artist.objects.get(name=artist_name)
    song_object = Song.objects.get(title=song_title)
    artist_object.songs.add(song_object)


remove object from db:

def remove_song_from_artist(artist_name: str, song_title: str):
    artist_object = Artist.objects.get(name=artist_name)
    song_object = Song.objects.get(title=song_title)
    artist_object.songs.remove(song_object)




case when:
from django.db.models import Case, When, IntegerField
from main_app.models import Dungeon


# for integers
Dungeon.objects.update(
    recommended_level=Case(
        When(difficulty='Easy', then=25),
        When(difficulty='Medium', then=50),
        When(difficulty='Hard', then=75),
        output_field=IntegerField(),
    )
)


# when choices and for non-numeric literals in the then clause.

def set_new_instructors():
    Workout.objects.update(
        instructor=Case(
            When(workout_type='Cardio', then=Value('John Smith')),
            When(workout_type='Strength', then=Value('Michael Williams')),
            When(workout_type='Yoga', then=Value('Emily Johnson')),
            When(workout_type='CrossFit', then=Value('Sarah Davis')),
            When(workout_type='Calisthenics', then=Value('Chris Heria')),
            output_field=CharField(),
        )
    )


relations in db:
class Department(models.Model):...
class Employee(models.Model):
...
department = models.ForeignKey(
	to=Department,
	on_delete=models.CASCADE, 
	related_name='employees'
	)


on delete option:

class Employee(models.Model):
...
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


many to many:
subjects = models.ManyToManyField(
		Subject, 
		through='StudentEnrollment'
		)



class Employee(models.Model):...
class Project(models.Model):
...
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
	
	
	
many to one = ForeignKey
CASCADE = delete all rows that reference

class StudentEnrollment(models.Model):
    student = models.ForeignKey(
        to='Student',
        on_delete=models.CASCADE)


one to one relation:
class LecturerProfile(models.Model):
    lecturer = models.OneToOneField(
        Lecturer,
        on_delete=models.CASCADE
    )



get something from the related table:
def calculate_average_rating_for_product_by_name(product_name: str):
    product_object = Product.objects.get(name=product_name)
    reviews_for_product = product_object.reviews.all()
    total_rating = sum(r.rating for r in reviews_for_product)
    avg_rating = total_rating / len(reviews_for_product)

    return avg_rating


get all objects with null values:
def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


dont create a db table model:
class Meta:
    abstract = True


proxy model:
class Meta:
    proxy = True
    
saving an instance to the DB
save()

def save(self, *args, **kwargs):
    super().save(*args, **kwargs)



data vlidation before saving
clean()
full_clean()

def clean(self):
    if self.specialty not in self.Specialization.choices:
        raise ValidationError('Specialty must be a valid choice.')


custom field:
class BooleanChoiceField(models.BooleanField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = ((True, 'Available'), (False, 'Not Available'))
        kwargs['default'] = True
        super().__init__(*args, **kwargs)


class StudentIDField(models.PositiveIntegerField):
    def to_python(self, value):
        try:
            return int(value)
        except ValueError:
            raise 'Invalid input for student ID'

    def get_prep_value(self, value):
        clean_value = self.to_python(value)

        if clean_value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')


validator example:
class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, message='Name must be at least 2 characters long.')
            MaxLengthValidator(100, message='Name cannot exceed 100 characters.')
        ]
    )


‘’'
MinValueValidator
MaxValueValidator
RegexValidator
EmailValidator
URLValidator
validate_ipv4_address
validate_ipv6_address
validate_ipv46_address
validate_coma_separated_integer_list
int_list_validator
DecimalValidator
FileExtensionValidator
‘’'

email = m.EmailField(
    error_messages={
        'invalid': 'Enter a valid email address'
    }
)



custom validator example:
def validate_menu_categories(value):
    required_categories = ["Appetizers", "Main Course", "Desserts"]
    missing_categories = [category for category in required_categories if category not in value]

    if missing_categories:
        raise ValidationError(
            'The menu must include each of the categories "Appetizers", "Main Course", "Desserts".')


validator in a class:
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


ordering inside models:
class Meta:
    ordering = ['-rating']
    verbose_name = 'Restaurant Review'
    verbose_name_plural = 'Restaurant Reviews'
    unique_together = ['reviewer_name', 'restaurant']
    

indexing
indexes = [
    Index(fields=['manu',], name='main_app_menu_review_menu_id')
]

models.Index


 shares the same database table as its parent model  
    class Meta:
        proxy = True

will not create table:
class Meta:
    abstract = True


mixin example:
class RechargeEnergyMixin:
    def recharge_energy(self, amount: int) -> None:
        self.energy = min(100, self.energy + amount)
        self.save()


class Hero(md, RechargeEnergyMixin):
    name = m.CharField(
        max_length=100,
    )
    hero_title = m.CharField(
        max_length=100,
    )
    energy = m.PositiveIntegerField()


manager example:
class ProductManager(models.Manager):
    def available_products(self):
        return self.filter(is_available=True)
    
    def available_products_in_category(self, category_name: str):
        return self.filter(category__name=category_name, is_available=True)
    
    
	in models model change the manager:
	objects = ProductManager()

Q objects operators:
 AND - & 
 OR - |
 NOT - ~
 XOR - ^
 
 example:
 products = Product.objects.filter(
    Q(is_available=True) &
    Q(price__gt=3)
).order_by(
    '-price',
    'name'
)


# Contain  the query in their title or their description.
@classmethod
def search_tasks(cls, query: str):
    return cls.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) 
    )


F objects (when we have logical AND we dont need Q, we use F):
product_to_be_discounted.update(price=F('price') * 0.7)

@classmethod
def ongoing_high_priority_task(cls):
    return cls.objects.filter(
        priority='High',
        is_completed=False,
        completion_date__gt=F('creation_date')
    )


 
annotate examples:
orders = Product.objects.annotate(
    total=Sum('orderproduct__quantity')
).values('name', 'total').order_by('-total')

 # returns the 2 most visited locations, ordered by location 
 # alphabetically (ascending). The most visited locations are
 # those with the most database records.
def popular_locations(self) -> QuerySet:
    return self.values('location').annotate(
        location_count=Count('location')
    ).order_by('-location_count', 'location')[:2]


#  returns the highest-rated game.

def highest_rated_game(self) -> QuerySet:
    return self.annotate(
        max_rating=Max('rating')
    ).order_by('-max_rating').first()


prefetch example (for stuff that is related tables, like manytomany relation):
orders = Order.objects.prefetch_related('orderproduct_set__product__category').order_by('id')

def get_programmers_with_technologies(self) -> QuerySet:
    return self.programmers.prefetch_related('projects__technologies_used')



raw example:
employees = Employee.objects.raw('SELECT * FROM users_employee')
