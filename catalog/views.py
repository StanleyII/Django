from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from catalog.films import Film, FilmBuilder, FilmsContainer
from catalog.database import DBConnect, PGFilmsManager


# Create your views here.
def main(request: HttpRequest):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')

    cursor = connect.cursor()
    query = """ SELECT * FROM films """
    cursor.execute(query)
    container = FilmsContainer()
    container.create_list_films(cursor.fetchall())
    data = container.get_list_films()
    count = len(data) if data is not None else 0
    cursor.close()

    cursor = connect.cursor()
    query = """ SELECT name_genre, translation FROM genres """
    cursor.execute(query)
    genres = {item[0]: "http://127.0.0.1:8000/catalog/genre/" + item[1] + '/' for item in cursor.fetchall()}
    cursor.close()

    context = {
        "data": data,
        "count": count,
        "genres": genres,
    }

    return render(request, template_name='films.html', context=context)


def get_by_genre(request: HttpRequest, genre=None):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')

    cursor = connect.cursor()
    query = """ SELECT name_genre, translation FROM genres """
    cursor.execute(query)
    data = cursor.fetchall()
    genre_data = {item[0]: item[1] for item in data}
    genres = {item[0]: "http://127.0.0.1:8000/catalog/genre/" + item[1] + '/' for item in data}
    cursor.close()

    if genre not in genre_data.values():

        context = {
            'count': 0,
            'genres': genres,
        }

        return render(request,
                      template_name='films.html',
                      context=context)
    else:
        params = (genre, )
        query = """ SELECT
                        films.film_id,
                        films.title,
                        genres.name_genre,
                        films.country,
                        films.director,
                        films.description,
                        films.rating,
                        films.cover
                    FROM 
                        films, genres
                    WHERE 
                        films.genre_id = genres.genre_id and
                        genres.translation = %s """

        cursor = connect.cursor()
        cursor.execute(query, params)
        films = cursor.fetchall()
        cursor.close()

        container = FilmsContainer()
        container.create_list_films(films)
        data = container.get_list_films()
        count = len(data) if data is not None else 0

        context = {
            "data": data,
            "count": count,
            "genres": genres,
        }

        return render(request,
                      template_name='films.html',
                      context=context)


def search_film(request: HttpRequest):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')
    cursor = connect.cursor()
    query = """ SELECT name_genre, translation FROM genres """
    cursor.execute(query)
    genres = {item[0]: "http://127.0.0.1:8000/catalog/genre/" + item[1] + '/' for item in cursor.fetchall()}
    cursor.close()

    if request.method == "GET":
        title = request.GET.get('title', '')

        if not title:
            context = {
                'count': 0,
                'genres': genres,
            }
        else:
            connect = DBConnect.get_connect(dbname='library_of_films',
                                            host='localhost',
                                            port=5432,
                                            user='postgres',
                                            password='postgres')

            builder = FilmBuilder()
            builder.create()
            builder.set_title(title)
            film = builder.get_film()

            data = PGFilmsManager.read(connect, film)
            count = len(data) if data is not None else 0
            context = {
                'data': data,
                'count': count,
                'genres': genres,
            }

        return render(request,
                      template_name='films.html',
                      context=context)


def search_film_by_genre(request: HttpRequest):

    genre = request.path.split('/')[3]
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')
    cursor = connect.cursor()
    query = """ SELECT name_genre, translation FROM genres """
    cursor.execute(query)
    genres = {item[0]: "http://127.0.0.1:8000/catalog/genre/" + item[1] + '/' for item in cursor.fetchall()}
    cursor.close()

    if request.method == "GET":
        title = request.GET.get('title', '')

        if not title:
            context = {
                'count': 0,
                'genres': genres,
            }
        else:
            params = (genre, "%" + title + "%")
            query = """ SELECT
                            films.film_id,
                            films.title,
                            genres.name_genre,
                            films.country,
                            films.director,
                            films.description,
                            films.rating,
                            films.cover
                        FROM 
                            films, genres
                        WHERE
                            films.genre_id = genres.genre_id AND 
                            genres.translation = %s AND 
                            films.title LIKE %s"""
            cursor = connect.cursor()
            cursor.execute(query, params)
            films = cursor.fetchall()

            container = FilmsContainer()
            container.create_list_films(films)
            data = container.get_list_films()
            count = len(data) if data is not None else 0
            cursor.close()

            context = {
                "data": data,
                "count": count,
                "genres": genres,
            }

        return render(request,
                      template_name='films.html',
                      context=context)


def redirect(request: HttpRequest):
    return render(request, '404.html')
