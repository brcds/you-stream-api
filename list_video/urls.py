from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from app_category.api.viewsets import CategoryViewSet
from app_video.api.viewsets import VideoViewSet
from app_video.views import CategoryVideosList

router = DefaultRouter()
router.register(r'videos', VideoViewSet, 'video')
router.register(r'categorias', CategoryViewSet, 'category')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/categorias/<int:category_id>/videos/', CategoryVideosList.as_view(), name='categoria-videos'),

]
