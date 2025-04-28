from rest_framework import serializers

class HaloSerializer(serializers.Serializer):
    nama = serializers.CharField(max_length=100)
    alamat = serializers.CharField(max_length=200)