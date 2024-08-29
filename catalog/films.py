from abc import ABC, abstractmethod


class Film:

    def __init__(self):

        self.film_id = None
        self.title = None
        self.genre = None
        self.country = None
        self.director = None
        self.actors = None
        self.description = None
        self.rating = None
        self.cover = None
        self.count = None


class Builder(ABC):

    @abstractmethod
    def create(self):
        ...

    @abstractmethod
    def set_film_id(self, film_id):
        ...

    @abstractmethod
    def set_title(self, title):
        ...

    @abstractmethod
    def set_genre(self, genre):
        ...

    @abstractmethod
    def set_country(self, country):
        ...

    @abstractmethod
    def set_director(self, director):
        ...

    @abstractmethod
    def set_actors(self, actors):
        ...

    @abstractmethod
    def set_description(self, description):
        ...

    @abstractmethod
    def set_rating(self, rating):
        ...

    @abstractmethod
    def set_cover(self, cover):
        ...

    @abstractmethod
    def set_count(self, count):
        ...

    @abstractmethod
    def get_film(self):
        ...


class FilmBuilder(Builder):

    _film: Film

    def create(self):
        self._film = Film()

    def set_film_id(self, film_id):
        self._film.film_id = film_id

    def set_title(self, title):
        self._film.title = title

    def set_genre(self, genre):
        self._film.genre = genre

    def set_country(self, country):
        self._film.country = country

    def set_director(self, director):
        self._film.director = director

    def set_actors(self, actors):
        self._film.actors = actors

    def set_description(self, description):
        self._film.description = description

    def set_rating(self, rating):
        self._film.rating = rating

    def set_cover(self, cover):
        self._film.cover = cover

    def set_count(self, count):
        self._film.count = count

    def get_film(self):
        return self._film


class FilmCreator:

    def __init__(self, builder: Builder):
        self._builder = builder

    def change_builder(self, builder: Builder):
        self._builder = builder

    def make(self, film: tuple) -> Film:
        self._builder.create()
        self._builder.set_film_id(film[0])
        self._builder.set_title(film[1])
        self._builder.set_genre(film[2])
        self._builder.set_country(film[3])
        self._builder.set_director(film[4])
        self._builder.set_actors(film[5])
        self._builder.set_description(film[6])
        self._builder.set_rating(film[7])
        img_path = str(film[8]) + '.jpg'
        self._builder.set_cover(img_path)
        self._builder.set_count(film[9])
        return self._builder.get_film()


class FilmsContainer:

    def __init__(self):
        self._films: list[Film] = []

    def create_list_films(self, data: list) -> None:
        builder = FilmBuilder()
        creator = FilmCreator(builder)

        for record in data:
            film = creator.make(record)
            self._films.append(film)

    def add_film(self, film: Film):
        self._films.append(film)

    def get_list_films(self):
        return self._films
