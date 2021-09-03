import uuid
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel


class Person(BaseModel):
    """
    model Person.
    """
    id: uuid.UUID
    full_name: str
    birth_date: Optional[datetime]


class Genre(BaseModel):
    """
    Genre model.
    """
    id: uuid.UUID
    name: str
    description: str


class FilmWork(BaseModel):
    """
    model FilmWork.
    """
    id: uuid.UUID
    title: str
    description: str
    creation_date: Optional[date]
    certificate: str
    rating: float
    type: str
    persons: List[Person]
    genres: List[Genre]


person_data = {
    'id': 'f50ec0b7-f960-400d-91f0-c42a6d44e3d0',
    'full_name': 'Alan Purdue',
    'birth_date': '2019-06-01 12:22',
}

genre_data = {
    'id': 'f50ec0b7-f960-400d-91f0-d41a4d24e3d0',
    'name': 'comedy',
    'description': 'This genre bring happy',
}

movies_data = {
    'id': 'f55fc2b7-f960-400d-91f0-d41a4d24e3d0',
    'title': 'Ace Ventura',
    'description': 'Cool detective who love animals, searching crime elements',
    'creation_date': '1997-01-01',
    'certificate': 'License MIT',
    'rating': 7.9,
    'type': 'film',
    'persons': [
        person_data
    ],
    'genres': [
        genre_data
    ]
}

person = Person(**person_data)
genre = Genre(**genre_data)
movie = FilmWork(**movies_data)

print(person)
print(genre)
print(movie)
