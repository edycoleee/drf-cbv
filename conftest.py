# conftest.py
import os
import django
import pytest

# Set environment variable before importing anything from Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Configure Django
django.setup()

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()