from django.contrib.auth.mixins import LoginRequiredMixin
# from django.db.models.query_utils import Q
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import ListView, FormView
import json
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
        modification_pk = self.kwargs.get('modification_pk', 0)
        current_modification = Modification.objects.get(pk=modification_pk)
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Комплектации', modification_info=current_modification)
        return {**context, **c_def}


class ShowWorkOrder(LoginRequiredMixin, DataMixin, FormView):
    form_class = SimpleForm
    template_name = 'autonorms/work-order.html'
    login_url = reverse_lazy('login')

    def get_works(self, equipment_pk: int, modification_pk: int, model_pk: int) -> dict:
        if equipment_pk:
            work_groups_ids = tuple(WorkGroup.objects.filter(
                equipment_id=equipment_pk).values_list('pk', flat=True))
        elif modification_pk:
            work_groups_ids = tuple(WorkGroup.objects.filter(
                modification_id=modification_pk).values_list('pk', flat=True))
        else:
            work_groups_ids = tuple(WorkGroup.objects.filter(
                model_id=model_pk).values_list('pk', flat=True))

        # works = Work.objects.filter(vehicle_unit__workgroup__pk__in=work_groups_ids).order_by('work_group__pk')
        works = Work.objects.select_related('vehicle_unit', 'vehicle_unit__workgroup').filter(
            vehicle_unit__workgroup__pk__in=work_groups_ids).order_by('work_group__pk')
        subworks = tuple(SubWork.objects.values('name', 'work__pk').filter(
            work__vehicle_unit__workgroup__pk__in=work_groups_ids))

        all_works = []
        dict_work = {}
        dict_vehicleunits = {}
        dict_work_groups = {}
        prev_workgroup = None

        for work in works:
            dict_work['name'] = work.name
            dict_work['pk'] = work.pk
            dict_work['vehicle_unit_pk'] = work.vehicle_unit.pk
            dict_work['work_group_pk'] = work.work_group.pk
            dict_work['subworks'] = [
                subwork for subwork in subworks if dict_work['pk'] == subwork['work__pk']]
            all_works.append(dict_work.copy())

            if prev_workgroup is None:
                prev_workgroup = work.vehicle_unit.workgroup.name

            if prev_workgroup == work.vehicle_unit.workgroup.name:
                dict_vehicleunits[work.vehicle_unit.name] = work.vehicle_unit.pk
            else:
                dict_work_groups[prev_workgroup] = dict_vehicleunits.copy()
                dict_vehicleunits.clear()
                dict_vehicleunits[work.vehicle_unit.name] = work.vehicle_unit.pk
                prev_workgroup = work.vehicle_unit.workgroup.name

        dict_work_groups[prev_workgroup] = dict_vehicleunits

        return dict_work_groups, all_works

    def get_auto_info(self, equipment_pk: int, modification_pk: int, model_pk: int) -> dict:
        auto_info = {'brand': '', 'model': '',
                     'modification': '', 'equipment': ''}

        if equipment_pk:
            auto_info['equipment'] = Equipment.objects.get(pk=equipment_pk)
            auto_info['modification'] = auto_info['equipment'].modification
            auto_info['model'] = auto_info['modification'].model
            auto_info['brand'] = auto_info['model'].brand
        elif modification_pk:
            auto_info['modification'] = Modification.objects.get(
                pk=modification_pk)
            auto_info['model'] = auto_info['modification'].model
            auto_info['brand'] = auto_info['model'].brand
        elif model_pk:
            auto_info['model'] = Model.objects.get(pk=model_pk)
            auto_info['brand'] = auto_info['model'].brand

        return auto_info

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        model_pk = self.request.GET.get('model', 0)
        modification_pk = self.request.GET.get('modification', 0)
        equipment_pk = self.request.GET.get('equipment', 0)
        dict_work_groups, all_works = self.get_works(
            equipment_pk, modification_pk, model_pk)
        auto_info = self.get_auto_info(equipment_pk, modification_pk, model_pk)
        c_def = self.get_user_context(
            title='Заказ-наряд', workgroups=dict_work_groups, works=all_works, auto_info=auto_info)
        return {**context, **c_def}

    def get(self, request, *args: str, **kwargs):
        # увеличу счетчик запросов в сессии
        request.session['number_requests'] = request.session.get(
            'number_requests', 0) + 1

        if self.check_requests_limit():
            return redirect('logout')

        return super().get(request, *args, **kwargs)


class AddWorkToOrder(LoginRequiredMixin, FormView):
    form_class = SimpleForm
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('work-order')

    def get_work_info(self) -> dict:
        work_info = {}
        serialized_data = json.loads(self.request.body)
        work_pk = serialized_data.get('work_pk', 0)

        if work_pk:
            work_info = Work.objects.values(
                'name', 'working_hour', 'pk',).get(pk=work_pk)
            work_info['subworks'] = tuple(SubWork.objects.values(
                'name', 'working_hour', 'pk', 'work_id', 'optional').filter(work_id=work_pk))

        return work_info

    def post(self, request, *args: str, **kwargs):
        work_info = self.get_work_info()
        return JsonResponse(work_info)
