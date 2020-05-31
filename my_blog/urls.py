"""my_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from article import views
from article import urls as article_urls
from django.views.static import serve
from django.conf import settings
from django.shortcuts import render, HttpResponse, redirect

from stark.service.stark import site


def foo(request):
    return HttpResponse('ok')


def test(request):
    return render(request, 'index2.html')


def get_urls():
    temp = []
    for model, admin_class in admin.site._registry.items():
        model_name = model._meta.model_name
        app_label = model._meta.app_label
        temp.append(path(r'%s/%s/'%(app_label,model_name,), (get_urls2(),None,None)))

        # temp.append((r'%s/5s'(model._meta.model_name,(model._meta.app_label)))
    return temp

def get_urls2():
    temp = []
    temp.append(re_path(r'^add/',add))
    temp.append(re_path('^(\d+)/delete/',delete))
    temp.append(re_path('^(\d+)/change/',change))
    temp.append(re_path(r'^$',list_view))
    return temp


def add(request):
    return HttpResponse('add')


def delete(request,id):
    return HttpResponse('delete')

def change(request,id):
    return HttpResponse('change')

def list_view(request):
    return HttpResponse('list_view')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('article/', include('article.urls', namespace='article')),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),

    path(r'register/', views.register),
    path(r'login/', views.login),
    path(r'logout/', views.logout),

    path(r'get_valid_img.png/', views.get_valid_img),

    path(r'index/', views.index),
    path(r'blog/', include(article_urls)),
    path('foo1/', foo, name='foo_name'),
    path(r'test/', (get_urls(), None,None)),
    path(r'stark/', site.urls)



]
