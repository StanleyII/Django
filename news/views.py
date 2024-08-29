from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse, HttpResponseRedirect
from news.news import News, NewsBuilder, NewsContainer
from catalog.database import DBConnect, PGFilmsManager

# Create your views here.


def main(request):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')

    cursor = connect.cursor()
    query = """ SELECT news_id, title, author, date, description, cover FROM news """
    cursor.execute(query)
    container = NewsContainer()
    container.create_list_news(cursor.fetchall())
    data = container.get_list_news()
    count = len(data) if data is not None else 0
    cursor.close()

    context = {
        "data": data,
        "count": count,
    }

    return render(request, template_name='all_news.html', context=context)


def news_detail(request: HttpRequest, news_detail):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')

    cursor = connect.cursor()

    query = """ SELECT
                        news.news_id,
                        news.title,
                        news.author,
                        news.date,
                        news.description,
                        news.cover
                    FROM 
                        news
                    WHERE 
                        news.news_id = %s"""
    params = (news_detail,)
    cursor.execute(query, params)
    container = NewsContainer()
    container.create_list_news(cursor.fetchall())
    data = container.get_list_news()

    cursor.close()

    context = {
        "data": data,
    }

    return render(request, template_name='page_news.html', context=context)


def new_page(request: HttpRequest):
    return render(request, template_name='new_page.html')
