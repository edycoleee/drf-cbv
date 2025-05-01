# belajar/urls.py
from django.urls import path
from .views import HaloView, NamaView

urlpatterns = [
    path('halo', HaloView.as_view(), name='halo'), # URL untuk endpoint halo
    path('nama/<str:nama>', NamaView.as_view(), name='nama'),# URL untuk endpoint nama
]
