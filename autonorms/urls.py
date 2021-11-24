from django.urls import path
from .views import *

urlpatterns = [
    path('autonorms/', ShowBrands.as_view(), name='autonorms'),
    path('model/brand<int:brand_pk>', ShowModels.as_view(), name='select_model'),
    path('modification/model<int:model_pk>', ShowModification.as_view(), name='select_modification'),
    path('equipment/equipment<int:modification_pk>', ShowEquipment.as_view(), name='select_equipment'),
    path('work-order', ShowWorkOrder.as_view(), name='work-order'),
    path('work_groups', ShowWorkGroups.as_view(), name='work_groups'),
]
