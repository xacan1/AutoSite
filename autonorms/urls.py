from django.urls import path
from .views import *

urlpatterns = [
    path('autonorms/', ShowBrands.as_view(), name='autonorms'),
    path('model/brand<int:brand_pk>', ShowModels.as_view(), name='select_model'),
    path('modification/model<int:model_pk>', ShowModification.as_view(), name='select_modification'),
]
