# product/tests.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestProductView:
    def test_get_all_products(self, api_client):
        # Insert data jika sql nanti

        url = reverse('product-url-list')  # pastikan ini sesuai dengan nama path di urls.py
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.data

        assert data["status"] == "success"
        assert data["message"] == "GET ALL PRODUCTS"
        #assert "products" in data["data"]
        #assert len(data["data"]["products"]) == 2
        assert len(data["data"]) == 2
        print(data)

        #names = [p["name"] for p in data["data"]["products"]]
        names = [p["prod_name"] for p in data["data"]]
        assert "Product 1" in names
        assert "Product 2" in names
    
