import os
import django
from django.db.models import QuerySet

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.core.management import call_command
from main_app.models import Pet, Artifact, Location, Car

call_command('makemigrations')
call_command('migrate')

def create_pet(name: str, species: str):
    Pet.objects.create(
        name=name,
        species=species
    )
    return f"{name} is a very cute {species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )
    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    artifacts = Artifact.objects.all()
    artifacts.delete()


def show_all_locations() -> str:
    all_locations = Location.objects.all().order_by('-id')
    return '\n'.join(str(loc) for loc in all_locations)


def new_capital() -> None:
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()


def get_capitals():
    # capitals = []
    # all_locations = Location.objects.all()
    # for loc in all_locations:
    #     if loc.is_capital:
    #         capitals.append(loc)
    # return capitals
    return Location.objects.filter(is_capital=True).values('name')


def delete_first_location():
    Location.objects.first().delete()


def apply_discount() -> None:
    all_cars = Car.objects.all()
    for car in all_cars:
        discount_percent = sum(int(digit) for digit in str(car.year)) / 100
        discount_price = float(car.price) * discount_percent
        car.price_with_discount = float(car.price) - discount_price
        car.save()


def get_recent_cars() -> QuerySet:
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    Car.objects.last().delete()


# Test prints

# print(create_pet('Buddy', 'Dog'))
# print(create_pet('Whiskers', 'Cat'))
# print(create_pet('Rocky', 'Hamster'))

# print(create_artifact('Ancient Sword', 'Lost Kingdom', 500, 'A legendary sword with a rich history', True))
# artifact_object = Artifact.objects.get(name='Ancient Sword')
# rename_artifact(artifact_object, 'Ancient Shield')
# print(artifact_object.name)

# print(show_all_locations())
# print(new_capital())
# print(get_capitals())

# print(apply_discount())
# print(get_recent_cars())