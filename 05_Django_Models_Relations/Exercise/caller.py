import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Author, Book, Artist, Song


# from dummy_data import populate_model_with_data
# populate_model_with_data(Song, 10)


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