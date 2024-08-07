from abc import ABC, abstractmethod


class Film:

    def __init__(self):

        self.title = None
        self.genre = None
        self.country = None
        self.director = None
        self.actors = []
        self.description = None
        self.rating = None
        self.cover = None


class Builder(ABC):

    @abstractmethod
    def create(self):
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
    def get_film(self):
        ...


class FilmBuilder(Builder):

    _film: Film

    def create(self):
        self._film = Film()

    def set_title(self, title):
        self._film.title = title

    def set_genre(self, genre):
        self._film.genre = genre

    def set_country(self, country):
        self._film.country = country

    def set_director(self, director):
        self._film.director = director

    def set_actors(self, actors):
        self._film.actors.extend(actors)

    def set_description(self, description):
        self._film.description = description

    def set_rating(self, rating):
        self._film.rating = rating

    def set_cover(self, cover):
        self._film.cover = cover

    def get_film(self):
        return self._film


class FilmCreator:

    def __init__(self, builder: Builder):
        self._builder = builder

    def change_builder(self, builder: Builder):
        self._builder = builder

    def make(self, film: tuple) -> Film:
        self._builder.create()
        self._builder.set_title(film[1])
        self._builder.set_genre(film[2])
        self._builder.set_country(film[3])
        self._builder.set_director(film[4])
        # self._builder.set_actors(film[5])
        self._builder.set_description(film[5])
        self._builder.set_rating(film[6])
        img_path = str(film[7]) + '.jpg'
        self._builder.set_cover(img_path)
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
