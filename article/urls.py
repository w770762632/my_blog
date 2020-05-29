from django.contrib import admin
from django.urls import path, include,re_path
from article import views
app_name = 'article'
urlpatterns = [
    path('', views.index),
    path('article_add/', views.article_add),
    re_path(r'(.*)/(\d+)/$', views.article_detail),
    re_path(r'(.*)/', views.home),  # home(request, username)
]
