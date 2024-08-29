from abc import ABC, abstractmethod
from datetime import date


class News:

    def __init__(self):

        self.news_id = None
        self.title = None
        self.author = None
        self.date = None
        self.description = None
        self.cover = None


class Builder(ABC):

    @abstractmethod
    def create(self):
        ...

    @abstractmethod
    def set_news_id(self, news_id):
        ...

    @abstractmethod
    def set_title(self, title):
        ...

    @abstractmethod
    def set_author(self, author):
        ...

    @abstractmethod
    def set_date(self, date):
        ...

    @abstractmethod
    def set_description(self, description):
        ...

    @abstractmethod
    def set_cover(self, cover):
        ...

    @abstractmethod
    def get_news(self):
        ...


class NewsBuilder(Builder):

    _news: News

    def create(self):
        self._news = News()

    def set_news_id(self, news_id):
        self._news.news_id = news_id

    def set_title(self, title):
        self._news.title = title

    def set_author(self, author):
        self._news.author = author

    def set_date(self, date):
        self._news.date = date

    def set_description(self, description):
        self._news.description = description

    def set_cover(self, cover):
        self._news.cover = cover

    def get_news(self):
        return self._news


class NewsCreator:

    def __init__(self, builder: Builder):
        self._builder = builder

    def change_builder(self, builder: Builder):
        self._builder = builder

    def make(self, news: tuple) -> News:
        self._builder.create()
        self._builder.set_news_id(news[0])
        self._builder.set_title(news[1])
        self._builder.set_author(news[2])
        self._builder.set_date(news[3])
        self._builder.set_description(news[4])
        img_path = str(news[5]) + '.jpg'
        self._builder.set_cover(img_path)
        return self._builder.get_news()


class NewsContainer:

    def __init__(self):
        self._news: list[News] = []

    def create_list_news(self, data: list) -> None:
        builder = NewsBuilder()
        creator = NewsCreator(builder)

        for record in data:
            news = creator.make(record)
            self._news.append(news)

    def add_news(self, news: News):
        self._news.append(news)

    def get_list_news(self):
        return self._news
