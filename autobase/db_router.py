from django.conf import settings

DATABASE_MAPPING = settings.DATABASE_APPS_MAPPING


class DatabaseAppsRouter:
    def db_for_read(self, model, **hints):
        return DATABASE_MAPPING.get(model._meta.app_label, None)

    def db_for_write(self, model, **hints):
        return DATABASE_MAPPING.get(model._meta.app_label, None)

    def allow_relation(self, obj1, obj2, **hints):
        result = None
        db_obj1 = DATABASE_MAPPING.get(obj1._meta.app_label, False)
        db_obj2 = DATABASE_MAPPING.get(obj2._meta.app_label, False)

        if db_obj1 and db_obj2:
            if db_obj1 == db_obj2:
                result = True
            else:
                result = False

        return result

    def allow_syncdb(self, db, model):
        result = None

        if db in DATABASE_MAPPING.values():
            result = DATABASE_MAPPING.get(model._meta.app_label, '') == db
        elif model._meta.app_label in DATABASE_MAPPING:
            result = False

        return result

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        result = None

        if db in DATABASE_MAPPING.values():
            result = DATABASE_MAPPING.get(app_label, '') == db
        elif app_label in DATABASE_MAPPING:
            result = False

        return result
