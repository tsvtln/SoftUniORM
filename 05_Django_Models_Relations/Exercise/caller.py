import os
from datetime import date, timedelta

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song, Product, Review, Driver, DrivingLicense, Owner, Car, \
    Registration


# from dummy_data import populate_model_with_data
# populate_model_with_data(Registration, 20)


# Create queries within functions

def show_all_authors_with_their_books():
    tp = []
    all_authors = Author.objects.all().order_by('id')
    for author in all_authors:
        books = Book.objects.filter(author=author)
        if books:
            writen_books = []
            for book in books:
                writen_books.append(book.title)
            tp.append(f"{author.name} has written - {', '.join(writen_books)}!")
    return '\n'.join(tp)


# print(show_all_authors_with_their_books())

def delete_all_authors_without_books():
    all_authors = Author.objects.all()
    for author in all_authors:
        book = Book.objects.filter(author=author)
        if not book:
            author.delete()
    # Author.objects.filter(book__isnull=True).delete()


# delete_all_authors_without_books()


### MUSIC APP ###

def add_song_to_artist(artist_name: str, song_title: str):
    artist_object = Artist.objects.get(name=artist_name)
    song_object = Song.objects.get(title=song_title)
    artist_object.songs.add(song_object)


# add_song_to_artist('Artist 1', 'Song 5')

def get_songs_by_artist(artist_name: str):
    return Artist.objects.get(name=artist_name).songs.all().order_by('-id')


# print(get_songs_by_artist('Artist 1'))

def remove_song_from_artist(artist_name: str, song_title: str):
    artist_object = Artist.objects.get(name=artist_name)
    song_object = Song.objects.get(title=song_title)
    artist_object.songs.remove(song_object)


# remove_song_from_artist('Artist 1', 'Song 5')


### SHOP ###
def calculate_average_rating_for_product_by_name(product_name: str):
    product_object = Product.objects.get(name=product_name)
    reviews_for_product = product_object.reviews.all()
    total_rating = sum(r.rating for r in reviews_for_product)
    avg_rating = total_rating / len(reviews_for_product)

    return avg_rating


# print(calculate_average_rating_for_product_by_name('Product 9'))


def get_reviews_with_high_ratings(threshold: int):
    return Review.objects.filter(rating__gte=threshold)


# print(get_reviews_with_high_ratings(50))

def get_products_with_no_reviews():
    return Product.objects.filter(reviews__isnull=True).order_by('-name')


# print(get_products_with_no_reviews())

def delete_products_without_reviews():
    Product.objects.filter(reviews__isnull=True).delete()


### LICENSE ###
def calculate_licenses_expiration_dates():
    return '\n'.join(
        [f"License with number: {lic.license_number} expires on {lic.issue_date + timedelta(days=365)}!" for lic in
         DrivingLicense.objects.all().order_by('-license_number')])


# print(calculate_licenses_expiration_dates())


def get_drivers_with_expired_licenses(due_date: date):
    expiration_date = due_date - timedelta(days=365)
    expired_licenses = Driver.objects.filter(
        license__issue_date__gt=expiration_date
    )
    return expired_licenses


# print(get_drivers_with_expired_licenses(date(2023, 1, 1)))


### CAR REGISTRATION ###
def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.owner = owner
    car.save()

    registration.registration_date = date.today()
    registration.car = car
    registration.save()

    return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."

# # Create owners
# owner1 = Owner.objects.create(name='Ivelin Milchev')
# owner2 = Owner.objects.create(name='Alice Smith')
#
# # Create cars
# car1 = Car.objects.create(model='Citroen C5', year=2004)
# car2 = Car.objects.create(model='Honda Civic', year=2021)
# # Create instances of the Registration model for the cars
# registration1 = Registration.objects.create(registration_number='TX0044XA')
# registration2 = Registration.objects.create(registration_number='XYZ789')
#
# print(register_car_by_owner(owner1))