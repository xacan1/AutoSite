from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView
from .models import *
from main.mixins import DataMixin


class ShowBrands(LoginRequiredMixin, DataMixin, ListView):
    model = Brand
    template_name = 'autonorms/brands.html'
    context_object_name = 'brands'
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Марки автомобилей')
        return {**context, **c_def}


class ShowModels(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'autonorms/models.html'
    context_object_name = 'models'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        brand_pk = self.kwargs.get('brand_pk', 0)
        return Model.objects.filter(brand_id=brand_pk)
        # return Brand.objects.get(pk=brand_pk).model_set.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        brand_pk = self.kwargs.get('brand_pk', 0)
        current_brand_name = Brand.objects.get(pk=brand_pk).name if brand_pk else ''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Модели автомобилей марки ' + current_brand_name)
        return {**context, **c_def}


class ShowModification(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'autonorms/modifications.html'
    context_object_name = 'modifications'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        model_pk = self.kwargs.get('model_pk', 0)
        return Modification.objects.filter(model_id=model_pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        model_pk = self.kwargs.get('model_pk', 0)
        current_model_name = Model.objects.get(pk=model_pk).name if model_pk else ''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Модификации модели ' + current_model_name)
        return {**context, **c_def}


class ShowEquipment(LoginRequiredMixin, RedirectView, DataMixin, ListView):
    template_name = 'autonorms/equipments.html'
    context_object_name = 'equipments'
    login_url = reverse_lazy('login')
    pattern_name = 'select_equipment'
    # url = 'http://127.0.0.1:8000'

    def get_queryset(self):
        modification_pk = self.kwargs.get('modification_pk', 0)
        result = Equipment.objects.filter(modification_id=modification_pk)

        if not result:
            self.get_redirect_url()

        return result

    def get_redirect_url(self, *args, **kwargs):
        modification_pk = self.kwargs.get('modification_pk', 0)
        result = Equipment.objects.filter(modification_id=modification_pk)
        if not result:
            return super().get_redirect_url(*args, **kwargs)




    def get_context_data(self, *, object_list=None, **kwargs):
        modification_pk = self.kwargs.get('modification_pk', 0)
        current_modification_name = Modification.objects.get(pk=modification_pk).name if modification_pk else ''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Комплектации')
        return {**context, **c_def}


# class GoToWorkTimes(RedirectView):
#     permanent = True
#     pattern_name = 'select_equipment'
#     url = 'http://127.0.0.1:8000/'
#
#     def get_redirect_url(self, *args, **kwargs):
#         return super().get_redirect_url(*args, **kwargs)


class ShowWorkTimes(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'autonorms/work-times.html'
    context_object_name = 'all_works'
    login_url = reverse_lazy('login')
