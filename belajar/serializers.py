# belajar/serializers.py
from rest_framework import serializers
#Serializer untuk input Halo
class HaloInputSerializer(serializers.Serializer):
    nama = serializers.CharField()
    alamat = serializers.CharField()

#Serializer Input dan Output untuk Message
class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

