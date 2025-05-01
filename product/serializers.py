#/product/serializer.py >>validation dan swagger input
from rest_framework import serializers

class ProductInputSerializer(serializers.Serializer):
    prod_name = serializers.CharField()
    price = serializers.FloatField()

class ProductOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    prod_name = serializers.CharField()
    price = serializers.FloatField()