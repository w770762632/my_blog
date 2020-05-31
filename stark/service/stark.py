from django.urls import path, include, re_path
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from django.forms import widgets as wid


class ModelSrark():
    list_display = ['__str__']
    list_display_link = []
    modelform_class = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def edit(self, obj=None, header=False):
        if header:
            return '编辑'

        _url = self.get_change_url(obj)
        return mark_safe('<a href="%s">编辑</a>' % _url)

    def deletes(self, obj=None, header=False):
        if header:
            return '删除'
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse('%s_%s_delete' % (app_label, model_name), args=(obj.pk,))
        return mark_safe('<a href="%s">删除</a>' % _url)

    def checkbox(self, obj=None, header=False):
        if header:
            return mark_safe('<input class="check" type="checkbox">')
        return mark_safe('<input class="check_item" type="checkbox">')

    def new_list_display(self):
        temp = []
        temp.append(ModelSrark.checkbox)
        temp.extend(self.list_display)
        if not self.list_display_link:
            temp.append(ModelSrark.edit)
        temp.append(ModelSrark.deletes)
        return temp

    def get_modelform_class(self):
        if not self.modelform_class:
            class ModelFormDemo(ModelForm):
                class Meta:
                    model = self.model
                    fields = '__all__'

            return ModelFormDemo
        else:
            return self.modelform_class

    def get_change_url(self, obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("%s_%s_change" % (app_label, model_name), args=(obj.pk,))

        return _url

    def get_delete_url(self, obj):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("%s_%s_delete" % (app_label, model_name), args=(obj.pk,))

        return _url

    def get_add_url(self):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("%s_%s_add" % (app_label, model_name))

        return _url

    def get_list_url(self):

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("%s_%s_list" % (app_label, model_name))

        return _url

    def add_view(self, request):
        ModelFormDemo = self.get_modelform_class()
        if request.method == "POST":
            form = ModelFormDemo(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            else:
                return render(request, "add_view.html", locals())

        form = ModelFormDemo()
        return render(request, "add_view.html", locals())

    def delete_view(self, request, id):
        if request.method == 'POST':
            del_obj = self.model.objects.filter(pk=id).first()
            del_obj.delete()
            return redirect(self.get_list_url())
        url = self.get_list_url()
        return render(request, 'delete_view.html')

    def change_view(self, request, id):
        edit_obj = self.model.objects.filter(pk=id).first()
        ModelFormDemo = self.get_modelform_class()

        if request.method == 'POST':
            form = ModelFormDemo(request.POST, instance=edit_obj)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request, 'change_view.html', locals())
        form = ModelFormDemo(instance=edit_obj)
        return render(request, 'change_view.html', locals())

    def list_view(self, request):

        data_list = self.model.objects.all()

        # 构建表头

        header_list = []
        for field in self.new_list_display():
            if callable(field):
                val = field(self, header=True)
                header_list.append(val)
            elif field == '__str__':
                header_list.append(self.model._meta.model_name.upper())
            else:
                val = self.model._meta.get_field(field).verbose_name
                header_list.append(val)

        new_data_list = []
        for obj in data_list:
            temp = []
            for field in self.new_list_display():
                if callable(field):
                    val = field(self, obj)
                else:
                    val = getattr(obj, field)
                    if field in self.list_display_link:
                        model_name = self.model._meta.model_name
                        app_label = self.model._meta.app_label
                        _url = reverse('%s_%s_change' % (app_label, model_name), args=(obj.pk,))
                        val = mark_safe('<a href = "%s">%s</a>' % (_url, val))
                temp.append(val)
            new_data_list.append(temp)
        return render(request, 'list_view.html', locals())

    def get_urls2(self):
        temp = []
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        temp.append(re_path(r'^add/', self.add_view, name='%s_%s_add' % (app_label, model_name)))
        temp.append(re_path('^(\d+)/delete/', self.delete_view, name='%s_%s_delete' % (app_label, model_name)))
        temp.append(re_path('^(\d+)/change/', self.change_view, name='%s_%s_change' % (app_label, model_name)))
        temp.append(re_path(r'^$', self.list_view, name='%s_%s_list' % (app_label, model_name)))
        return temp

    @property
    def urls2(self):
        return self.get_urls2(), None, None


class AdminSite():
    def __init__(self):
        self._registry = {}
        self.app_name = 'stark'
        self.namespace = 'stark'

    def register(self, model, stark_class=None):
        if not stark_class:
            stark_class = ModelSrark
        self._registry[model] = stark_class(model, self)

    def get_urls(self):
        temp = []
        for model, stark_class in self._registry.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            # 分发增删改查
            temp.append(re_path(r'^%s/%s/' % (app_label, model_name), stark_class.urls2))
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


site = AdminSite()
