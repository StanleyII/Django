from abc import ABC, abstractmethod
from .films import Film, FilmsContainer
import psycopg2


class DBConnect:

    _instance = None

    @classmethod
    def get_connect(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = psycopg2.connect(*args, **kwargs)
        return cls._instance


class DBManager(ABC):

    @staticmethod
    @abstractmethod
    def create(connect, book: Film):
        ...

    @staticmethod
    @abstractmethod
    def read(connect, film: Film):
        ...

    @staticmethod
    @abstractmethod
    def update(connect, old_film: Film, new_film: Film):
        ...

    @staticmethod
    @abstractmethod
    def delete(connect, film: Film):
        ...


class PGFilmsManager(DBManager):

    @staticmethod
    def create(connect, film: Film):
        # Вызвать запрос вставки данных из объекта в таблицу
        ...

    @staticmethod
    def read(connect, film: Film) -> list[Film]:

        try:
            with connect.cursor() as cursor:

                params = (film.title, )
                query = """SELECT * 
                           FROM films
                           WHERE title = %s"""
                cursor.execute(query, params)
                data = cursor.fetchall()

                if data:
                    container = FilmsContainer()
                    container.create_list_films(data)
                    return container.get_list_films()
                else:
                    raise Exception(f"Не найдена запись с параметрами {params}")
        except (Exception, psycopg2.Error) as e:
            print(e)

    @staticmethod
    def update(connect, index_old_film: int, new_film: Film):
        # Обновить данные о фильме в таблице
        ...

    @staticmethod
    def delete(connect, film: Film):
        # Удалить фильм
        ...