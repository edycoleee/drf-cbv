from django.shortcuts import render

# Create your views here.
# belajar/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaloInputSerializer, MessageResponseSerializer
from drf_spectacular.utils import extend_schema

class HaloView(APIView):
    @extend_schema(
        responses=MessageResponseSerializer
    )
    def get(self, request):
        return Response({"message": "Belajar DRF CBV"}, status=status.HTTP_200_OK)
    #Schema untuk request dan response >> apenAPI
    @extend_schema(
        request=HaloInputSerializer,
        responses=HaloInputSerializer
    )
    def post(self, request):
        # Serializer untuk validasi input
        serializer = HaloInputSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NamaView(APIView):
    @extend_schema(
        responses=MessageResponseSerializer
    )
    def get(self, request, nama):
        return Response({"message": f"Halo {nama}"}, status=status.HTTP_200_OK)
