from django.contrib import admin
from article import models


# Register your models here.

class UserInfoConfig(admin.ModelAdmin):
    list_display = ['username', 'phone']


class ArticleConfig(admin.ModelAdmin):
    list_display = ['title', 'desc',]

class CategoryConfig(admin.ModelAdmin):
    list_display = ['title', 'blog',]

class ArticleDetailConfig(admin.ModelAdmin):
    list_display = ['content', 'article_id', ]


admin.site.register(models.UserInfo, UserInfoConfig)
admin.site.register(models.Blog)
admin.site.register(models.ArticleDetail,ArticleDetailConfig)

admin.site.register(models.Article, ArticleConfig)
admin.site.register(models.Category, CategoryConfig)

