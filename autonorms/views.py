from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import reset_queries
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView
from .forms import SimpleForm
from .models import *
from main.mixins import DataMixin


class ShowBrands(LoginRequiredMixin, DataMixin, ListView):
    model = Brand
    template_name = 'autonorms/brands.html'
    context_object_name = 'brands'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs) -> dict:
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

    def get_context_data(self, **kwargs) -> dict:
        brand_pk = self.kwargs.get('brand_pk', 0)
        current_brand_name = Brand.objects.get(
            pk=brand_pk).name if brand_pk else ''
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Модели автомобилей марки ' + current_brand_name)
        return {**context, **c_def}


class ShowModification(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'autonorms/modifications.html'
    context_object_name = 'modifications'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        model_pk = self.kwargs.get('model_pk', 0)
        return Modification.objects.filter(model_id=model_pk)

    def get_context_data(self, **kwargs) -> dict:
        model_pk = self.kwargs.get('model_pk', 0)
        current_model_name = Model.objects.get(
            pk=model_pk).name if model_pk else ''
        context = super().get_context_data(**kwargs)
        qs = context.get('object_list')
        exists_equipment = qs and Equipment.objects.filter(
            modification_id=qs[0].pk)
        c_def = self.get_user_context(
            title='Модификации модели ' + current_model_name, exists_equipment=exists_equipment)
        return {**context, **c_def}


class ShowEquipment(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'autonorms/equipments.html'
    context_object_name = 'equipments'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        modification_pk = self.kwargs.get('modification_pk', 0)
        return Equipment.objects.filter(modification_id=modification_pk)

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Комплектации')
        return {**context, **c_def}


class ShowWorkOrder(LoginRequiredMixin, DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'autonorms/work-order.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Оформление заказ-наряда')
        return {**context, **c_def}


class ShowWorkGroups(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'autonorms/work_groups.html'
    context_object_name = 'work_groups'
    login_url = reverse_lazy('login')

    def get_queryset(self):
        equipment_pk = self.request.GET.get('equipment', 0)
        modification_pk = self.request.GET.get('modification', 0)

        if equipment_pk:
            qs = WorkGroup.objects.filter(equipment_id=equipment_pk)
        else:
            qs = WorkGroup.objects.filter(modification_id=modification_pk)

        return qs