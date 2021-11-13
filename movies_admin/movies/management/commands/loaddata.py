import random
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import factory
from faker import Faker
from factory.django import DjangoModelFactory
from ...models import Genre, Person, FilmWork, PersonFilmWork, FilmWorkGenre

data_persons = []
data_films = []
data_genres = []

genres = [
    "криминал",
    "комедия",
    "мелодрама",
    "драма",
    "триллер",
    "ужасы",
    "исторический фильм",
    "чёрный юмор",
    "фильм-сказка",
    "cемейный фильм",
]

fake = Faker()


def create_manytomany_list(model, data_space):
    """create list from models."""
    queryset = model.objects.all()
    for i in queryset:
        data_space.append(i)


def get_queryset_person():
    """return queryset from PersonRole model."""
    return Person.objects.get(id=data_persons[random.randint(0, 99999)].id)


def get_queryset_genres():
    """return queryset from FilmWorkGenre model."""
    return FilmWorkGenre.objects.get(id=data_genres[random.randint(0, 9)].id)


def create_new_objects(factory_model, model_django, count):
    """create objects for models"""
    while count != 0:
        if count < 500:
            count -= 10
            build = factory_model.build_batch(10)
            model_django.objects.bulk_create(build)
        else:
            count -= 500
            build = factory_model.build_batch(500)
            model_django.objects.bulk_create(build)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    username = factory.Sequence(lambda n: "username{}".format(n))
    email = factory.Faker("email")


class GenreFactory(DjangoModelFactory):
    class Meta:
        model = Genre

    id = factory.Faker("uuid4")
    name = factory.Sequence(lambda n: genres[n])
    description = factory.Faker("text")


class PersonRoleFactory(DjangoModelFactory):
    class Meta:
        model = Person

    id = factory.Faker("uuid4")
    full_name = factory.Faker("name")
    birth_date = factory.Faker("date_of_birth")


class FilmWorkFactory(DjangoModelFactory):
    class Meta:
        model = FilmWork

    id = factory.Faker("uuid4")
    title = factory.Sequence(lambda n: "film{}".format(n))
    description = factory.Faker("text")
    creation_date = factory.Faker("date")
    rating = fake.random_int(min=1.0, max=10.0)
    type = fake.random_element(elements=("movie", "tv_show"))


class PersonFilmWorkFactory(DjangoModelFactory):
    class Meta:
        model = PersonFilmWork

    id = factory.Faker("uuid4")
    film_work = factory.Sequence(lambda n: data_films[n])
    person = factory.LazyFunction(get_queryset_person)
    role = fake.random_element(elements=("director", "actor", "writer"))


class FilmWorkGenreFactory(DjangoModelFactory):
    class Meta:
        model = FilmWorkGenre

    id = factory.Faker("uuid4")
    film_work = factory.Sequence(lambda n: data_films[n])
    genre = factory.LazyFunction(get_queryset_genres)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("started filling in the database")
        create_new_objects(GenreFactory, Genre, 10)
        print("create 10 new genres")
        create_new_objects(PersonRoleFactory, Person, 100000)
        print("create 100000 new persons")
        create_new_objects(FilmWorkFactory, FilmWork, 1000000)
        print("create 1000000 new films")
        create_manytomany_list(Person, data_persons)
        print("create list persons")
        create_manytomany_list(FilmWork, data_films)
        print("create list films")
        create_new_objects(PersonFilmWorkFactory, PersonFilmWork, 1000000)
        print("created 1000000 connections for the PersonFilmWork model")
        create_new_objects(FilmWorkGenreFactory, FilmWorkGenre, 1000000)
        print("created 1000000 connections for the FilmWorkGenre model")
        print("finished generating the data")
