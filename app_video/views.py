from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response
from .models import Video
from app_video.api.serializers import VideoSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CategoryVideosList(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Video.objects.filter(category_id=category_id)

    def list(self, request, *args, **kwargs):
        videos = self.get_queryset()
        page = self.paginate_queryset(videos)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({"videos": serializer.data})

        serializer = VideoSerializer(videos, many=True)
        return Response({"videos": serializer.data})


class VideosFreeList(generics.ListAPIView):

    serializer_class = VideoSerializer

    def get_queryset(self):
        queryset = Video.objects.order_by("?")[:5]
        return queryset
