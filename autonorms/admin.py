from django.contrib import admin
from . import models


admin.site.register(models.Brand)
admin.site.register(models.Model)
admin.site.register(models.Modification)
admin.site.register(models.Equipment)
admin.site.register(models.WorkGroup)
admin.site.register(models.VehicleUnit)
admin.site.register(models.Work)
admin.site.register(models.SubWork)
admin.site.register(models.Part)
