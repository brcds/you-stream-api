import pytest
from rest_framework.test import APIClient
from rest_framework import status

from .models import Video
from app_category.models import Category

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def category():
    Category.objects.create(title_category="LIVRE", color="VERDE")
    Category.objects.create(title_category="ADULTO", color="VERMELHO")

@pytest.fixture
def video():
    video = Video.objects.create(title="test", description="test", url='http://test.com')
    return video


@pytest.mark.django_db
def test_create_video(api_client, category):
    esperado = status.HTTP_201_CREATED
    video = api_client.post(
        '/api/videos/', data={'title': 'test', 'description': 'test', 'url': 'http://teste.com'}, format='json'
    )
    print(video.data)
    assert esperado == video.status_code

@pytest.mark.django_db
def test_create_video_with_category(api_client, category):
    esperado = status.HTTP_201_CREATED
    video = api_client.post(
        '/api/videos/',
        data={'title': 'test', 'description': 'test', 'url': 'http://teste.com', 'category': 2},
        format='json'
    )
    print(video.data)
    assert esperado == video.status_code

@pytest.mark.django_db
def test_update_video(api_client, category, video):
    esperado = status.HTTP_200_OK
    video_editado = api_client.put(
        path=f'/api/videos/{video.id}/',
        data={'title': 'testEditado', 'description': 'test', 'url': 'http://teste.com', 'category': 2},
        format='json'
    )
    print(video_editado.data)
    assert esperado == video_editado.status_code

@pytest.mark.django_db
def test_patch_video(api_client, category, video):
    esperado = status.HTTP_200_OK
    video_patched = api_client.patch(
        path=f'/api/videos/{video.id}/',
        data={'title': 'Video TESTE 001'},
        format='json'
    )
    print(video_patched.data)
    assert esperado == video_patched.status_code

@pytest.mark.django_db
def test_delete_video(api_client, category, video):
    video_deleted = api_client.delete(
        path=f'/api/videos/{video.id}/',
        format='json'
    )
    print(video_deleted.data)
    assert video_deleted.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_search_video_title(api_client, video):
    esperado = status.HTTP_200_OK
    resultado = api_client.get(
        path=f'/api/videos/?search=test',
        format='json'
    )
    print(resultado.data)
    assert esperado == resultado.status_code



