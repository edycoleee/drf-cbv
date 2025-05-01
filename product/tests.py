# product/tests.py
from django.db import connection
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# === Fixtures ===
@pytest.fixture(scope="session", autouse=True)
def create_test_table(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prod_name TEXT NOT NULL,
                    price REAL NOT NULL
                )
            """)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_products():
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO tb_products ( prod_name, price) VALUES ('macbook', 100)")
        cursor.execute("INSERT INTO tb_products ( prod_name, price) VALUES ('surface', 200)")
    yield
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM tb_products")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='tb_products'")  # reset autoincrement
        

# === Test Class ===
@pytest.mark.django_db
class TestProductView:

    def test_get_all_products(self, api_client, setup_products):
        url = reverse('product-url-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "success"
        names = [p["prod_name"] for p in response.data["data"]]
        assert "macbook" in names and "surface" in names

    def test_get_single_product(self, api_client, setup_products):
        url = reverse('product-url-detail', args=[1])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["prod_name"] == "macbook"

    def test_create_product(self, api_client):
        url = reverse('product-url-list')
        payload = {"prod_name": "New Product", "price": 15.5}
        response = api_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["prod_name"] == "New Product"

    def test_update_product(self, api_client, setup_products):
        url = reverse('product-url-detail', args=[1])
        payload = {"prod_name": "Updated Product", "price": 99.9}
        response = api_client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["prod_name"] == "Updated Product"

    def test_delete_product(self, api_client, setup_products):
        url = reverse('product-url-detail', args=[1])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_product_invalid_name(self, api_client):
        url = reverse('product-url-list')
        payload = {"prod_name": "", "price": 10.0}
        response = api_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "prod_name" in response.data