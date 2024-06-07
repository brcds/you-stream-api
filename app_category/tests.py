import pytest
from rest_framework import status
from rest_framework.test import APIClient

from app_video.models import Video
from .models import Category


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def category_id():
    category = Category.objects.create(
        title_category="Test Category", color="test color"
    )
    return category.id


@pytest.fixture
def create_video_and_category():
    category1 = Category.objects.create(title_category="Livre", color="Verde")
    category2 = Category.objects.create(title_category="Adulto", color="Vermelho")

    list_category = [category1, category2]
    for category in list_category:
        Video.objects.create(
            category=category,
            title=f"test video-{category}",
            description=f"test video-{category}",
            url=f"http://test.com/{category}",
        )


@pytest.mark.django_db
def test_create_category(api_client):
    esperado = status.HTTP_201_CREATED
    category = api_client.post(
        "/api/categorias/",
        {"title_category": "Adulto", "color": "Vermelho"},
        format="json",
    )
    print(category.content)
    assert category.status_code == esperado


@pytest.mark.django_db
def test_list_category(api_client):
    esperado = status.HTTP_200_OK
    category = api_client.get(
        "/api/categorias/",
        format="json",
    )
    print(category.content)
    assert category.status_code == esperado


@pytest.mark.django_db
def test_retrieve_category(api_client, category_id):
    esperado = status.HTTP_200_OK
    category = api_client.get(
        f"/api/categorias/1/",
        format="json",
    )
    print(category.content)
    assert category.status_code == esperado


@pytest.mark.django_db
def test_update_category(api_client, category_id):
    esperado = status.HTTP_200_OK
    category = api_client.put(
        "/api/categorias/1/",
        {"title_category": "Adulto", "color": "Vermelho"},
        format="json",
    )
    print(category.content)
    assert category.status_code == esperado


@pytest.mark.django_db
def test_patch_category(api_client, category_id):
    esperado = status.HTTP_200_OK
    category = api_client.patch(
        "/api/categorias/1/",
        {"title_category": "Comedia"},
        format="json",
    )
    print(category.content)
    assert category.status_code == esperado


@pytest.mark.django_db
def test_delete_category(api_client, category_id):
    esperado = status.HTTP_200_OK
    category = api_client.delete(
        "/api/categorias/1/",
        format="json",
    )
    print(category.content)
    assert category.status_code == esperado


@pytest.mark.django_db
def test_list_video_category(api_client, create_video_and_category):
    esperado = status.HTTP_200_OK
    category = api_client.get(
        "/api/categorias/1/videos/",
        format="json",
    )
    print(category.content)
    assert category.status_code == esperado
