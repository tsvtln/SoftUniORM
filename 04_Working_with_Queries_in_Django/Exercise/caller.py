import os
from typing import List

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop


def show_highest_rated_art() -> str:
    all_arts = ArtworkGallery.objects.all().order_by('-rating', 'id').first()
    return f"{all_arts.art_name} is the highest-rated art with a {all_arts.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([
        first_art,
        second_art,
    ])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop():
    all_laptops = Laptop.objects.all().order_by('-price', '-id').first()
    return f"{all_laptops.brand} is the most expensive laptop available for {all_laptops.price}$!"


def bulk_create_laptops(args: List[Laptop]):
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage() -> None:
    # lenovo_laptops = Laptop.objects.all().filter(brand='Lenovo')
    # asus_laptops = Laptop.objects.all().filter(brand='Asus')
    # for update_storage in lenovo_laptops:
    #     update_storage.storage = 512
    #     update_storage.save()
    #
    # for update_storage in asus_laptops:
    #     update_storage.storage = 512
    #     update_storage.save()
    Laptop.objects.filter(brand__in=["Asus", "Lenovo"]).update(storage=512)


def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)


def update_operation_systems() -> None:
    Laptop.objects.filter(brand='Asus').update(operation_system=Laptop.OperatingSystems.WINDOWS)
    Laptop.objects.filter(brand='Apple').update(operation_system=Laptop.OperatingSystems.MACOS)
    Laptop.objects.filter(brand__in=['Dell', 'Acer']).update(operation_system=Laptop.OperatingSystems.LINUX)
    Laptop.objects.filter(brand='Lenovo').update(operation_system=Laptop.OperatingSystems.CHROMEOS)


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()
