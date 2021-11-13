from django.views.generic import ListView
from .models import *
from main.mixins import DataMixin


class ShowBrands(DataMixin, ListView):
    model = Brand
    template_name = 'autonorms/brands.html'
    context_object_name = 'brands'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Марки автомобилей')
        return {**context, **c_def}


class ShowModels(DataMixin, ListView):
    template_name = 'autonorms/models.html'
    context_object_name = 'models'

    def get_queryset(self):
        brand_pk = self.kwargs.get('brand_pk', 0)
        return Model.objects.filter(brand_id=brand_pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Модели автомобилей')
        return {**context, **c_def}


class ShowModification(DataMixin, ListView):
    template_name = 'autonorms/modifications.html'
    context_object_name = 'modifications'

    def get_queryset(self):
        model_pk = self.kwargs.get('model_pk', 0)
        return Modification.objects.filter(model_id=model_pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Модификации')
        return {**context, **c_def}
