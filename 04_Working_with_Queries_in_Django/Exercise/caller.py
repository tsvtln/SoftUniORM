import os
from typing import List

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import Case, When, CharField, Value
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout


# from dummy_data import populate_model_with_data
#
# populate_model_with_data(Workout, 20)

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

### MEAL ###
def set_new_chefs():
    Meal.objects.filter(meal_type='Breakfast').update(chef='Gordon Ramsay')
    Meal.objects.filter(meal_type='Lunch').update(chef='Julia Child')
    Meal.objects.filter(meal_type='Dinner').update(chef='Jamie Oliver')
    Meal.objects.filter(meal_type='Snack').update(chef='Thomas Keller')


# set_new_chefs()


def set_new_preparation_times():
    Meal.objects.filter(meal_type='Breakfast').update(preparation_time='10 minutes')
    Meal.objects.filter(meal_type='Lunch').update(preparation_time='12 minutes')
    Meal.objects.filter(meal_type='Dinner').update(preparation_time='15 minutes')
    Meal.objects.filter(meal_type='Snack').update(preparation_time='5 minutes')


# set_new_preparation_times()

def update_low_calorie_meals():
    Meal.objects.filter(meal_type__in=['Breakfast', 'Dinner']).update(calories='400')


# update_low_calorie_meals()


def update_high_calorie_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).update(calories='700')


# update_high_calorie_meals()


def delete_lunch_and_snack_meals():
    Meal.objects.filter(meal_type__in=['Lunch', 'Snack']).delete()


### DUNGEON ###


def show_hard_dungeons():
    hard_dungeons = Dungeon.objects.all().filter(difficulty='Hard').order_by('-location')
    tp = [f"{dungeon.name} is guarded by {dungeon.boss_name} who has {dungeon.boss_health} health points!" for dungeon
          in hard_dungeons]
    return '\n'.join(tp)


# print(show_hard_dungeons())

def bulk_create_dungeons(args: List[Dungeon]):
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.filter(difficulty='Easy').update(name='The Erased Thombs')
    Dungeon.objects.filter(difficulty='Medium').update(name='The Coral Labyrinth')
    Dungeon.objects.filter(difficulty='Hard').update(name='The Lost Haunt')


# update_dungeon_names()

def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty='Easy').update(boss_health=500)


# update_dungeon_bosses_health()


def update_dungeon_recommended_levels():
    Dungeon.objects.filter(difficulty='Easy').update(recommended_level=25)
    Dungeon.objects.filter(difficulty='Medium').update(recommended_level=50)
    Dungeon.objects.filter(difficulty='Hard').update(recommended_level=75)


# update_dungeon_recommended_levels()

def update_dungeon_rewards():
    Dungeon.objects.filter(boss_health=500).update(reward='1000 Gold')
    Dungeon.objects.filter(location__startswith='E').update(reward='New dungeon unlocked')
    Dungeon.objects.filter(location__endswith='s').update(reward='Dragonheart Amulet')


# update_dungeon_rewards()

def set_new_locations():
    Dungeon.objects.filter(recommended_level=25).update(location='Enchanted Maze')
    Dungeon.objects.filter(recommended_level=50).update(location='Grimstone Mines')
    Dungeon.objects.filter(recommended_level=75).update(location='Shadowed Abyss')


# set_new_locations()


### WORKOUT ###

def show_workouts():
    cali_cross = Workout.objects.all().filter(workout_type__in=['Calisthenics', 'CrossFit']).order_by('id')
    tp = [f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!" for w in cali_cross]
    return '\n'.join(tp)


# print(show_workouts())

def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(
        workout_type='Cardio',
        difficulty='High'
    ).order_by('instructor')


# print(get_high_difficulty_cardio_workouts())

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


# set_new_instructors()

def set_new_duration_times():
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
            output_field=CharField(),
        )
    )


# set_new_duration_times()

def delete_workouts():
    Workout.objects.exclude(workout_type__in=['Strength', 'Calisthenics']).delete()
