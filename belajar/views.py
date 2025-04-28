from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import HaloSerializer

class HaloView(APIView):
    def get(self, request):
        return Response({"message": "Belajar DRF"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HaloSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NamaView(APIView):
    def get(self, request, nama=None):
        if not nama:
            return Response(
                {"error": "Nama tidak diberikan."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": f"Halo {nama}"}, status=status.HTTP_200_OK)

# Create your views here.
