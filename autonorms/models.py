from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, verbose_name='Брэнд')
    full_loading = models.BooleanField(default=False, verbose_name='Загружено полностью')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Брэнд'
        verbose_name_plural = 'Брэнды'
        ordering = ['name']


class Model(models.Model):
    name = models.CharField(max_length=100, blank=False, verbose_name='Модель')
    full_loading = models.BooleanField(default=False, verbose_name='Загружено полностью')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
        ordering = ['name']


class Modification(models.Model):
    name = models.CharField(max_length=50, verbose_name='Модификация')
    year = models.CharField(max_length=50, verbose_name='Год')
    horsepower = models.FloatField(null=False, verbose_name='Мощность, л.с.')
    engine_power = models.FloatField(null=False, verbose_name='Мощность, кВт')
    engine_code = models.CharField(max_length=50, verbose_name='Код двигателя')
    engine_volume = models.FloatField(null=False, verbose_name='Объем, см³')
    car_body = models.CharField(max_length=100, verbose_name='Кузов')
    full_loading = models.BooleanField(default=False, verbose_name='Загружено полностью')
    model = models.ForeignKey(Model, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}-{self.year}-{self.horsepower}-{self.engine_code}'

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Модификация'
        verbose_name_plural = 'Модификации'
        ordering = ['name']


class Equipment(models.Model):
    name = models.CharField(max_length=50, verbose_name='Комплектация')
    full_loading = models.BooleanField(default=False, verbose_name='Загружено полностью')
    modification = models.ForeignKey(Modification, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Комплектация'
        verbose_name_plural = 'Комплектации'
        ordering = ['name']


class WorkGroup(models.Model):
    name = models.CharField(max_length=100, verbose_name='Группа работ')
    equipment = models.ForeignKey(Equipment, on_delete=models.PROTECT)
    modification = models.ForeignKey(Modification, on_delete=models.PROTECT)
    model = models.ForeignKey(Model, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Группа работ'
        verbose_name_plural = 'Группы работ'
        ordering = ['name']


class VehicleUnit(models.Model):
    name = models.CharField(max_length=100, verbose_name='Узел')
    workgroup = models.ForeignKey(WorkGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Узел'
        verbose_name_plural = 'Узлы'
        ordering = ['name']


class Work(models.Model):
    name = models.CharField(max_length=150, verbose_name='Работа')
    work_number = models.CharField(max_length=20, verbose_name='Каталожный номер')
    working_hour = models.FloatField(null=False, verbose_name='Норма времени')
    description = models.TextField(blank=True, verbose_name='Описание')
    vehicle_unit = models.ForeignKey(VehicleUnit, on_delete=models.PROTECT)
    work_group = models.ForeignKey(WorkGroup, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        # ordering = ['name']


class SubWork(models.Model):
    name = models.CharField(max_length=150, verbose_name='Составная работа')
    work_number = models.CharField(max_length=20, verbose_name='Каталожный номер')
    working_hour = models.FloatField(null=False, verbose_name='Норма времени')
    description = models.TextField(blank=True, verbose_name='Описание')
    optional = models.BooleanField(default=False, verbose_name='Опциональная')
    work = models.ForeignKey(Work, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Составная работа'
        verbose_name_plural = 'Составные работы'
        # ordering = ['name']


class Part(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    part_number = models.CharField(max_length=25, verbose_name='Артикул')
    work_number = models.CharField(max_length=20, verbose_name='Каталожный номер работы')
    model = models.ForeignKey(Model, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'autonorms'
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'
        ordering = ['name']

