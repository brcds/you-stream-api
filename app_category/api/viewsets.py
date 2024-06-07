from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from app_category.api.serializers import CategorySerializer
from app_category.models import Category
from django.http import Http404
from rest_framework.exceptions import ValidationError

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class CategoryViewSet(ModelViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        categories = self.get_queryset()
        page = self.paginate_queryset(categories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({"categorias": serializer.data})

        serializer = self.get_serializer(categories, many=True)
        return Response({"categorias": serializer.data})

    def retrieve(self, request, pk=None, **kwargs):
        queryset = self.get_queryset()
        categoria = queryset.filter(pk=pk).first()
        if categoria:
            serializer = CategorySerializer(categoria)
            return Response({"detail": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Categoria não encontrado"}, status=404)

    def create(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Video Incluido com Sucesso!"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            categoria = self.get_object()
            serializer = self.get_serializer(
                categoria, data=request.data, partial=False
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"detail": "Categoria Editado com sucesso!.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {"detail": "Categoria não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def partial_update(self, request, *args, **kwargs):
        try:
            categoria = self.get_object()
            serializer = self.get_serializer(categoria, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {"detail": "Categoria Editado com sucesso!.", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        try:
            video = self.get_object()
            self.perform_destroy(video)
            return Response(
                {"detail": "Categoria deletado com sucesso!."},
                status=status.HTTP_200_OK,
            )
        except Http404:
            return Response(
                {"detail": "Categoria não encontrado."},
                status=status.HTTP_404_NOT_FOUND,
            )
