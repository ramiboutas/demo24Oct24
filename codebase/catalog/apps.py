from django.apps import AppConfig


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "codebase.catalog"

    def ready(self):  # pragma: no cover
        from . import signals  # noqa
