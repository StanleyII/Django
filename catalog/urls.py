from django.urls import path
from catalog.views import main
from catalog.views import get_by_genre, search_film

urlpatterns = [
    path('', main),
    path('genre/<str:genre>/', get_by_genre),
]