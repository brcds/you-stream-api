from rest_framework import viewsets, status
from app_video.api.serializers import VideoSerializer
from app_video.models import Video
from rest_framework.response import Response
from django.http import Http404
from rest_framework.exceptions import ValidationError


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = Video.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(title__icontains=search)
        return queryset

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Video.objects.all()
        video = queryset.filter(pk=pk).first()
        if video:
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        else:
            return Response({"detail": "Video não encontrado"}, status=404)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Video Incluido com Sucesso!", "video": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            video = self.get_object()
            serializer = self.get_serializer(video, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({
                'detail': 'Video Editado com sucesso!.',
                'data': serializer.data},
                status=status.HTTP_200_OK
            )
        except Http404:
            return Response({'detail': 'Video não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, *args, **kwargs):
        try:
            video = self.get_object()
            serializer = self.get_serializer(video, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response({'detail': 'Video Editado com sucesso!.', 'data': serializer.data},
                status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            video = self.get_object()
            self.perform_destroy(video)
            return Response({'detail': 'Video deletado com sucesso!.'}, status=status.HTTP_200_OK)
        except Http404:
            return Response({'detail': 'Video não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
