from django.contrib import admin
from app_video.models import Video


class VideoAdmin(admin.ModelAdmin):
    ...


admin.site.register(Video, VideoAdmin)