from django.shortcuts import render
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse, HttpResponseRedirect

from news.database import PGNewsManager
from news.news import News, NewsBuilder, NewsContainer, NewsCreator
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
                        news.news_id != %s
                    ORDER BY
                        news.date DESC
                    LIMIT 4"""

    params = (news_detail,)
    cursor.execute(query, params)
    container = NewsContainer()
    container.create_list_news(cursor.fetchall())
    data_ex = container.get_list_news()

    cursor.close()

    context = {
        "data": data,
        "data_ex": data_ex,
        "len_count": len(data_ex),
    }

    return render(request, template_name='page_news.html', context=context)


def new_page(request: HttpRequest):
    return render(request, template_name='new_page.html')


def create_news(request: HttpRequest):
    connect = DBConnect.get_connect(dbname='library_of_films',
                                    host='localhost',
                                    port=5432,
                                    user='postgres',
                                    password='postgres')
    if request.method == "POST":
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        cover = request.POST.get('cover', '')
        date_p = request.POST.get('date', '')
        author = request.POST.get('author', '')

        cursor = connect.cursor()
        query = """ SELECT COUNT(*) FROM news """
        cursor.execute(query)
        value = cursor.fetchall()

        params_news = (int(value[0][0]) + 1, title, author, date_p, description, cover)
        # print(params_news)
        news_builder = NewsBuilder()
        news = NewsCreator(news_builder)
        make_news = news.make(params_news, new_news=True)
        PGNewsManager.create(connect, make_news)
        connect.commit()

    return HttpResponseRedirect('/news/')
