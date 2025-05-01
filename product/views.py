#product/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from myproject.utils.custom_exception import NotFoundException
from myproject.utils.response_wrapper import success_response
from product.serializers import ProductInputSerializer
from product.services import ProductService
from product.schemas import (
    product_list_schema,
    product_create_schema,
    product_retrieve_schema,
    product_update_schema,
    product_delete_schema,    

)

class ProductViewSet(viewsets.ViewSet):

    @product_list_schema
    def list(self, request):
        products = ProductService.get_all_products()
        return Response(success_response("GET ALL PRODUCTS",products))


    @product_retrieve_schema
    def retrieve(self, request, pk=None):
        product = ProductService.get_product_by_id(pk)
        if not product:
            raise NotFoundException('Product not found')
        return Response(success_response("GET SINGLE PRODUCT",product))

    @product_create_schema
    def create(self, request):
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_product = ProductService.create_product(data['prod_name'], data['price'])
        return Response(success_response("ADD NEW PRODUCT",new_product), status=status.HTTP_201_CREATED)

    @product_update_schema
    def update(self, request, pk=None):
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        updated_product = ProductService.update_product(pk, data['prod_name'], data['price'])
        if not updated_product:
            raise NotFoundException('Product not found')
        return Response(success_response("UPDATED PRODUCT",updated_product))

    @product_delete_schema
    def destroy(self, request, pk=None):
        deleted = ProductService.delete_product(pk)
        if not deleted:
            raise NotFoundException('Product not found')
        return Response(success_response("DELETED PRODUCT",{"deleted": True}), status=status.HTTP_204_NO_CONTENT)