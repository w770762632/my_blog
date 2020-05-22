from django import forms
from article import models
from django.core.exceptions import ValidationError
import re


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class RegForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        label='用户名',
        error_messages={
            'required': '用户名不能为空',
            'max_length': '用户名最长16位',
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control"},
        )
    )
    phone = forms.CharField(
        max_length=11,
        label='手机号码',
        required=False,
        validators=[mobile_validate, ],
        error_messages={
            'max_length': '手机号码不能超过11位',
            "invalid": "号码格式不正确！",
        },
        widget=forms.widgets.TextInput(
            attrs={"class": "form-control"},

        )

    )
    password = forms.CharField(
        min_length=6,
        label='密码',
        error_messages={
            'required': '密码不能为空',
            'min_length': '密码至少要6位',
        },
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},

        )
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(
            attrs={"class": "form-control"},
            render_value=True,
        ),
        error_messages={
            "min_length": "确认密码至少要6位！",
            "required": "确认密码不能为空",
        }
    )
    email = forms.EmailField(
        label="邮箱",
        widget=forms.widgets.EmailInput(
            attrs={"class": "form-control"},

        ),
        error_messages={
            "invalid": "邮箱格式不正确！",
            "required": "邮箱不能为空",
        }
    )

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if re_password and re_password != password:
            self.add_error("re_password", ValidationError("两次密码不一致"))

        else:
            return self.cleaned_data

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(set(password)) == 1:
            raise ValidationError('密码太简单了')
        return password

    def clean_re_password(self):
        re_password = self.cleaned_data.get('re_password')
        if len(set(re_password)) == 1:
            raise ValidationError('确认密码太简单了')
        return re_password

    def clean_username(self):
        username = self.cleaned_data.get('username')
        ret = models.UserInfo.objects.filter(username=username).count()
        if ret:
            raise ValidationError('用户名已存在')
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            ret = models.UserInfo.objects.filter(phone=phone).count()
            if ret:
                raise ValidationError('手机号码已存在')
            return phone
        else:
            return phone
