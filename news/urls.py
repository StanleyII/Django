from django.urls import path

import news.views

urlpatterns = [
    path('', news.views.main),
    path('<int:news_detail>/', news.views.news_detail, name='news_detail'),
    path('new_page/', news.views.new_page)
]