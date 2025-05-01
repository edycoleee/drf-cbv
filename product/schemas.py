#product/schemas.py
from drf_spectacular.utils import extend_schema, OpenApiExample
from product.serializers import ProductInputSerializer, ProductOutputSerializer


# Example Object (bisa reusable)
product_example = OpenApiExample(
    'Product Example',
    value={
        "id": 1,
        "prod_name": "Produk Contoh",
        "price": 10000
    },
    request_only=False,  # tampil di response
    response_only=False, # tampil di request
)

product_create_example = OpenApiExample(
    'Create Product Example',
    value={
        "prod_name": "Produk Baru",
        "price": 15000
    },
    request_only=True,  # hanya tampil di request body
)

# List Products
product_list_schema = extend_schema(
    responses=ProductOutputSerializer(many=True),
    summary="List all products",
    description="Retrieve a list of all products.",
    examples=[product_example],
    tags=["Products"],
    request=None,  # tidak ada request body    
)

# Create Product
product_create_schema = extend_schema(
    request=ProductInputSerializer,
    responses=ProductOutputSerializer,
    summary="Create a new product",
    description="Create a new product with name and price.",
    examples=[product_create_example, product_example],
    tags=["Products"],
)

# Retrieve Product
product_retrieve_schema = extend_schema(
    responses=ProductOutputSerializer,
    summary="Retrieve a product by ID",
    description="Retrieve product details by its ID.",
    examples=[product_example],
    tags=["Products"],
)

# Update Product
product_update_schema = extend_schema(
    request=ProductInputSerializer,
    responses=ProductOutputSerializer,
    summary="Update a product by ID",
    description="Update an existing product by its ID.",
    examples=[product_create_example, product_example],
    tags=["Products"],
)

# Delete Product
product_delete_schema = extend_schema(
    responses=None,
    summary="Delete a product by ID",
    description="Delete an existing product by its ID.",
    tags=["Products"],
)
