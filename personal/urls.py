from django.urls import path

import personal.views
from .views import main

urlpatterns = [
    path('', personal.views.main),
    path('delete/<int:delete_film>/', personal.views.delete_film, name='delete_film'),
]