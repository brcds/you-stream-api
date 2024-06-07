from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Category


@receiver(post_migrate)
def create_categories(sender, **kwargs):
    if sender.name == "app_category":
        Category.objects.get_or_create(
            id=1, defaults={"title_category": "LIVRE", "color": "VERDE"}
        )
