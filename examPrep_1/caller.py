import os
import django
from django.db.models import Max, Count, Avg, Q, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# dummy data
# from main_app.models import Director, Actor, Movie
# from dummy_data import populate_model_with_data
# populate_model_with_data(Movie, 20)

# Import your models here

from main_app.models import Director, Actor, Movie


# Create queries within functions


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ''
    #
    # directors_list = []
    # tp = []
    # all_directors = Director.objects.all().order_by('full_name')
    #
    # if search_name and search_nationality:
    #     for director in all_directors:
    #         if director.full_name == search_name and director.nationality == search_nationality:
    #             directors_list.append(director)
    #
    # elif search_name and search_nationality is None:
    #     for director in all_directors:
    #         if director.full_name == search_name:
    #             directors_list.append(director)
    #
    # elif search_name is None and search_nationality:
    #     for director in all_directors:
    #         if director.nationality == search_nationality:
    #             directors_list.append(director)

    query = Q()
    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query |= query_name & query_nationality
    elif search_name is not None:
        query |= query_name
    else:
        query |= query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ''

    result = []

    [result.append(f"Director: {director.full_name}, nationality: {director.nationality}, "
                   f"experience: {director.years_of_experience}") for director in directors]

    return '\n'.join(result)

    # for i in directors_list:
    #     tp.append(f'Director: {i.full_name}, nationality: {i.nationality}, experience: {i.years_of_experience}')
    #
    # return '\n'.join(tp)


def get_top_director():
    max_movies_count = Director.objects.get_directors_by_movies_count().aggregate(max_count=Max('movies_count'))[
        'max_count'].order_by('full_name')
    if max_movies_count is None:
        return ''
    tp = []
    directors_with_max_movies = Director.objects.annotate(
        movies_count=Count('movies_directed')
    ).filter(movies_count=max_movies_count)
    for director in directors_with_max_movies:
        tp.append(f'Top Director: {director.full_name}, movies: {director.movies_count}.')
        break
    return '\n'.join(tp)


def get_top_actor():
    actor = Actor.objects.prefetch_related('starred_movies') \
        .annotate(
        num_of_movies=Count('starred_movies'),
        movies_avg_rating=Avg('starred_movies__rating')) \
        .order_by('-num_of_movies', 'full_name') \
        .first()

    if not actor or not actor.num_of_movies:
        return ""

    movies = ", ".join(movie.title for movie in actor.starred_movies.all() if movie)

    return f"Top Actor: {actor.full_name}, starring in movies: {movies}, " \
           f"movies average rating: {actor.movies_avg_rating:.1f}"


def get_actors_by_movies_count():
    actors = Actor.objects.annotate(num_movies=Count('movies_acted_in')) \
                 .order_by('-num_movies', 'full_name')[:3]

    if not actors or not actors[0].num_movies:
        return ""

    result = []
    for actor in actors:
        result.append(f"{actor.full_name}, participated in {actor.num_movies} movies")

    return '\n'.join(result)


def get_top_rated_awarded_movie():
    top_movie = Movie.objects \
        .select_related('starring_actor') \
        .prefetch_related('actors') \
        .filter(is_awarded=True) \
        .order_by('-rating', 'title') \
        .first()

    if not top_movie:
        return ""

    starring_actor = top_movie.starring_actor.full_name if top_movie.starring_actor else "N/A"

    participating_actors = top_movie.actors.order_by('full_name').values_list('full_name', flat=True)
    cast = ", ".join(participating_actors) if participating_actors else "N/A"

    return f"Top rated awarded movie: {top_movie.title}, rating: {top_movie.rating:.1f}. " \
           f"Starring actor: {starring_actor}. Cast: {cast}."


def increase_rating():
    updated_movies = Movie.objects.filter(is_classic=True, rating__lt=10.0)

    if not updated_movies:
        return "No ratings increased."

    num_of_updated_movies = updated_movies.update(rating=F('rating') + 0.1)

    return f"Rating increased for {num_of_updated_movies} movies."

# test prints
# print(get_directors(None, 'BG'))
# print(get_top_director())
# print(get_top_actor())
# print(get_top_rated_awarded_movie())
# print(increase_rating())
# print(Director.objects.get_directors_by_movies_count())
# print(get_directors(search_name='S', search_nationality=None))
# print(get_top_actor())
# print(get_actors_by_movies_count())
# print(get_top_rated_awarded_movie())