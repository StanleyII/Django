from django.shortcuts import render
from django.http import HttpRequest

from catalog.database import DBConnect
from catalog.films import FilmsContainer


# Create your views here.


def main(request: HttpRequest):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')

    cursor = connect.cursor()
    query = """ SELECT films.film_id,
                        films.title,
                        genres.name_genre,
                        films.country,
                        films.director,
                        films.actors,
                        films.description,
                        films.rating,
                        films.cover,
                        films.count
                    FROM films, favorites, genres 
                    WHERE favorites.user_id = %s AND films.film_id = favorites.film_id
                    AND films.genre_id = genres.genre_id """
    params = (1,)
    cursor.execute(query, params)
    container = FilmsContainer()
    container.create_list_films(cursor.fetchall())
    data = container.get_list_films()
    count = len(data) if data is not None else 0
    cursor.close()

    context = {
        "data": data,
    }

    return render(request, template_name='favorites.html', context=context)
