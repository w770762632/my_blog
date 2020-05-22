from django.test import TestCase

# Create your tests here.
import os

# 在py中测试ORM的代码环境搭建：
if __name__ == '__main__':
    # 加载django项目的配置信息
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_blog.settings')
    # 导Django 并 启动Django项目
    import django

    django.setup()
    from article import models
    from django.db.models import Count

    user = models.UserInfo.objects.filter(nid=13).first()
    print(user)
    # ret = models.Article.objects.create(title='111111', desc='22222', user__id=user)
    # print(ret)
    # ret = models.Article.objects.filter(user__nid=13)
    # print(ret)
    blog = user.blog
    category_list = models.Category.objects.filter(blog__userinfo__nid=13).annotate(c=Count("article")).values("title", "c")
    print(category_list)