from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter

from app_category.api.viewsets import CategoryViewSet
from app_video.api.viewsets import VideoViewSet
from app_video.views import CategoryVideosList
from app_video.views import VideosFreeList

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"videos", VideoViewSet, "video")
router.register(r"categorias", CategoryViewSet, "category")


urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api/categorias/<int:category_id>/videos/",
        CategoryVideosList.as_view(),
        name="categoria-videos",
    ),
    path(
        "api/videos/free",
        VideosFreeList.as_view(),
        name="video-free",
    ),
]
