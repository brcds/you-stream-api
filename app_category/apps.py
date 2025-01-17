from django.apps import AppConfig


class AppCategoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app_category"

    def ready(self):
        import app_category.signals
