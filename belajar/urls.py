#/belajar/urls.py
from django.urls import path
from .views import HaloView, NamaView

urlpatterns = [
    path('halo', HaloView.as_view(), name='halo-get'),
    path('halo', HaloView.as_view(), name='halo-post'),  # sama endpoint, beda method
    path('nama/<str:nama>', NamaView.as_view(), name='nama-get'),
]