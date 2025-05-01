# belajar/tests.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestHaloView:
    def test_get_halo(self, api_client):
        url = reverse('halo')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"message": "Belajar DRF CBV"}
    
    def test_post_halo_valid_data(self, api_client):
        url = reverse('halo')
        data = {
            "nama": "Silmi",
            "alamat": "Semarang"
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == data
    
    def test_post_halo_invalid_data(self, api_client):
        url = reverse('halo')
        data = {
            "nama": "",  # invalid - empty string
            "alamat": "Semarang"
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "nama" in response.data  # error message for nama field

# @pytest.mark.django_db
# class TestNamaView:
#     def test_get_nama(self, api_client):
#         nama = "Silmi"
#         url = reverse('nama', kwargs={'nama': nama})
#         response = api_client.get(url)
        
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {"message": f"Halo {nama}"}
