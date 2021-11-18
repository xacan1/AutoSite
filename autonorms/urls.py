from django.urls import path
from .views import *

urlpatterns = [
    path('autonorms/', ShowBrands.as_view(), name='autonorms'),
    path('model/brand<int:brand_pk>', ShowModels.as_view(), name='select_model'),
    path('modification/model<int:model_pk>', ShowModification.as_view(), name='select_modification'),
    path('equipment/equipment<int:modification_pk>', ShowEquipment.as_view(), name='select_equipment'),
    # path('work-times/', GoToWorkTimes.as_view(), name='go_to_work_times'),
    path('work-times/', ShowWorkTimes.as_view(), name='work-times'),
]
