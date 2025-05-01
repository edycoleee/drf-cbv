import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from pytest_drf.util import url_for

@pytest.mark.django_db
class TestAPI:
    client = APIClient()

    def test_get_halo(self):
        url = url_for('halo')  # /halo
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json() == {"message": "Belajar DRF"}

    def test_get_nama(self):
        url = url_for('nama', args=["Silmi"])  # /nama/Silmi
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json() == {"message": "Halo Silmi"}

    def test_post_halo_valid(self):
        url = url_for('halo')  # /halo
        data = {
            "nama": "Silmi",
            "alamat": "Semarang"
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 200
        assert response.json() == data

    def test_post_halo_invalid(self):
        url = url_for('halo')
        data = {
            "nama": "Silmi"
            # alamat tidak ada
        }
        response = self.client.post(url, data, format='json')
        assert response.status_code == 400
        assert "alamat" in response.json()
