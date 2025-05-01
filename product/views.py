#product/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from myproject.utils.response_wrapper import success_response
from product.schemas import (
    product_list_schema,
)

class ProductViewSet(viewsets.ViewSet):

    @product_list_schema
    def list(self, request):
        products = [
                {
                    "id": 1,
                    "prod_name": "Product 1",
                    "price": 10.0,
                },
                {
                    "id": 2,
                    "prod_name": "Product 2",
                    "price": 20.0,
                },
            ]
        return Response(success_response("GET ALL PRODUCTS",products))