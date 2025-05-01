#product/schemas.py
from drf_spectacular.utils import extend_schema, OpenApiExample
from product.serializers import ProductOutputSerializer


# Example Object (bisa reusable)
product_example = OpenApiExample(
    'Product Example',
    value={
        "id": 1,
        "name": "Produk Contoh",
        "price": 10000.0
    },
    request_only=False,  # tampil di response
    response_only=False, # tampil di request
)

product_create_example = OpenApiExample(
    'Create Product Example',
    value={
        "name": "Produk Baru",
        "price": 15000.0
    },
    request_only=True,  # hanya tampil di request body
)

# List Products
product_list_schema = extend_schema(
    responses=ProductOutputSerializer(many=True),
    summary="List all products",
    description="Retrieve a list of all products.",
    examples=[product_example],
)