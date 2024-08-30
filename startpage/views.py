from typing import List, Dict, Any

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from catalog.films import Film, FilmBuilder, FilmsContainer
from catalog.database import DBConnect, PGFilmsManager
from news.news import NewsContainer, NewsBuilder

# Create your views here.


def get_list_slides(data) -> list[dict[str, int | Any] | dict[str, int | Any] | dict[str, int | Any] | dict[str, int | Any] | dict[str, int | Any]]:

    slides = [
        {
            'counter': 0,
            'title': data[0].title,
            'description': data[0].description,
            'image': "static/img/covers/" + data[0].cover,
        },
        {
            'counter': 1,
            'title': data[1].title,
            'description': data[1].description,
            'image': "static/img/covers/" + data[1].cover,
        },
        {
            'counter': 2,
            'title': data[2].title,
            'description': data[2].description,
            'image': "static/img/covers/" + data[2].cover,
        },
        {
            'counter': 3,
            'title': data[3].title,
            'description': data[3].description,
            'image': "static/img/covers/" + data[3].cover,
        },
        {
            'counter': 4,
            'title': data[4].title,
            'description': data[4].description,
            'image': "static/img/covers/" + data[4].cover,
        },
    ]

    return slides


def main(request: HttpRequest):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')

    cursor = connect.cursor()
    query = """ SELECT
                        films.film_id,
                        films.title,
                        genres.name_genre,
                        films.country,
                        films.director,
                        films.actors,
                        films.description,
                        films.rating,
                        films.cover,
                        films.count
                    FROM 
                        films, genres
                    WHERE 
                        films.genre_id = genres.genre_id
                    ORDER BY
                        films.rating
                    LIMIT 5"""
    cursor.execute(query)
    container = FilmsContainer()
    container.create_list_films(cursor.fetchall())
    top_films = container.get_list_films()

    top_films = get_list_slides(top_films)

    # print(top_films)

    query = """ SELECT * FROM news ORDER BY date DESC LIMIT 4 """
    cursor.execute(query)

    container = NewsContainer()
    container.create_list_news(cursor.fetchall())
    top_news = container.get_list_news()

    cursor.close()

    context = {
        "top_films": top_films,
        "top_news": top_news,
    }

    return render(request, template_name='page.html', context=context)
