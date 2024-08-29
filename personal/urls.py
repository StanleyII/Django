from django.urls import path

import personal.views
from .views import main

urlpatterns = [
    path('', personal.views.main),
]