from abc import ABC, abstractmethod
from .news import News, NewsContainer
import psycopg2


class DBManager(ABC):

    @staticmethod
    @abstractmethod
    def create(connect, news: News):
        ...

    @staticmethod
    @abstractmethod
    def read(connect, news: News):
        ...

    @staticmethod
    @abstractmethod
    def update(connect, old_news: News, new_news: News):
        ...

    @staticmethod
    @abstractmethod
    def delete(connect, news: News):
        ...


class PGNewsManager(DBManager):

    @staticmethod
    def create(connect, news: News):
        # Вызвать запрос вставки данных из объекта в таблицу
        try:
            with connect.cursor() as cursor:
                params = (news.news_id, news.title, news.author, news.date, news.description, news.cover[:len(news.cover)-4])
                query = """ 
                        INSERT INTO news(news_id, title, author, date, description, cover)
                        VALUES (%s, %s, %s, %s, %s, %s)

                        """
                cursor.execute(query, params)
        except (Exception, psycopg2.Error) as e:
            print(e)

    @staticmethod
    def read(connect, news: News) -> list[News]:

        try:
            with connect.cursor() as cursor:

                params = (news.title, )
                query = """SELECT * 
                           FROM news
                           WHERE title = %s"""
                cursor.execute(query, params)
                data = cursor.fetchall()

                if data:
                    container = NewsContainer()
                    container.create_list_films(data)
                    return container.get_list_news()
                else:
                    raise Exception(f"Не найдена запись с параметрами {params}")
        except (Exception, psycopg2.Error) as e:
            print(e)

    @staticmethod
    def update(connect, index_old_news: int, new_news: News):
        # Обновить данные о новости в таблице
        ...

    @staticmethod
    def delete(connect, news: News):
        # Удалить новость
        ...