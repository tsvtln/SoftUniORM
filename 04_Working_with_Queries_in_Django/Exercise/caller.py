import os
from typing import List

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import ArtworkGallery, Laptop, ChessPlayer


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


def bulk_create_chess_players(args: List[ChessPlayer]):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    no_title_chess_players = ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    # all_players = ChessPlayer.objects.all()
    # for player in all_players:
    #     if player.title == 'GM':
    #         player.games_won = 30
    #         player.save()
    ChessPlayer.objects.filter(title="GM").update(games_won=30)


def change_chess_games_lost():
    no_title_players = ChessPlayer.objects.filter(title='no title')
    for player in no_title_players:
        player.games_lost = 25
        player.save()


def change_chess_games_drawn():
    all_players = ChessPlayer.objects.all()
    for player in all_players:
        player.games_drawn = 10
        player.save()


def grand_chess_title_GM():
    high_rated_players = ChessPlayer.objects.filter(rating__gte=2400)
    for player in high_rated_players:
        player.title = 'GM'
        player.save()


def grand_chess_title_IM():
    mid_range_players = ChessPlayer.objects.filter(rating__range=(2300, 2399))
    for player in mid_range_players:
        player.title = 'IM'
        player.save()


def grand_chess_title_FM():
    low_rated_players = ChessPlayer.objects.filter(rating__range=(2200, 2299))
    for player in low_rated_players:
        player.title = 'FM'
        player.save()


def grand_chess_title_regular_player():
    regular_players = ChessPlayer.objects.filter(rating__range=(0, 2199))
    for player in regular_players:
        player.title = 'regular player'
        player.save()
#
#
# player1 = ChessPlayer(
#     username='Player1',
#     title='no title',
#     rating=2200,
#     games_played=50,
#     games_won=20,
#     games_lost=25,
#     games_drawn=5,
# )
# player2 = ChessPlayer(
#     username='Player2',
#     title='IM',
#     rating=2350,
#     games_played=80,
#     games_won=40,
#     games_lost=25,
#     games_drawn=15,
# )
#
# # Call the bulk_create_chess_players function
# bulk_create_chess_players([player1, player2])
#
# # Call the delete_chess_players function
# delete_chess_players()
#
# # Check that the players are deleted
# print("Number of Chess Players after deletion:", ChessPlayer.objects.count())
