# belajar/serializers.py

from rest_framework import serializers

class HaloInputSerializer(serializers.Serializer):
    nama = serializers.CharField()
    alamat = serializers.CharField()

class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

