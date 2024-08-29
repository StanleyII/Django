from django.urls import path

import catalog.views
from catalog.views import main
from catalog.views import get_by_genre, search_film, film_detail

urlpatterns = [
    path('', main),
    path('genre/<str:genre>/', get_by_genre),
    path('<int:film_detail>/', catalog.views.film_detail, name='film_detail'),
]