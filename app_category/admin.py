from django.contrib import admin

from app_category.models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin): ...


admin.site.register(Category, CategoryAdmin)
