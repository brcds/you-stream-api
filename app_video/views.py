from rest_framework import generics
from rest_framework.response import Response
from .models import Video
from app_video.api.serializers import VideoSerializer


class CategoryVideosList(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Video.objects.filter(category_id=category_id)

    def list(self, request, *args, **kwargs):
        videos = self.get_queryset()
        serializer = VideoSerializer(videos, many=True)
        return Response({"videos": serializer.data})


