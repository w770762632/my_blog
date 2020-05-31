from stark.service.stark import site, ModelSrark
from article import models

from django.forms import ModelForm


class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'
        labels = {
            'username': '用户名',
        }


class UserInfoConfig(ModelSrark):
    list_display = ['nid', 'username', 'phone', ]
    list_display_link = ['username']
    modelform_class = UserInfoModelForm


site.register(models.UserInfo, UserInfoConfig)

site.register(models.Article)
