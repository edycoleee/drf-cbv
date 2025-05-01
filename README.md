### 1. GITHUB

```cmd
echo "# drf-cbv" >> README.md
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/drf-cbv.git
git push -u origin main
```

### 2. API SEDERHANA

#### 2.1 API SPECS

GET http://127.0.0.1:8000/halo Response: { "message": "Belajar DRF CBV" }

GET http://127.0.0.1:8000/nama/Silmi Response: { "message": "Halo Silmi" }

POST http://127.0.0.1:8000/halo

Body:

```json
{
  "nama": "Silmi",
  "alamat": "Semarang"
}
```

Response:

```json
{
  "nama": "Silmi",
  "alamat": "Semarang"
}
```

Dokumentasi Swagger http://127.0.0.1:8000/docs/ → untuk tampilan Swagger UI.

#### 2.2 Virtual Environment dan Install Django + DRF

```py
# Buat folder project
mkdir belajar-drf
cd belajar-drf

# Buat virtual environment
python -m venv venv

# Aktifkan venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Django dan Django REST Framework + drf-spectacular(Swagger) + pytest-drf(Testing)
pip install django djangorestframework pytest pytest-django drf-spectacular

# Start Django project
django-admin startproject myproject .

# Buat app bernama "belajar"
python manage.py startapp belajar

```

```cmd

```

#### 2.3 Setting Django (myproject/settings.py)

```py
INSTALLED_APPS = [
    ...
    'rest_framework',
    'drf_spectacular',
    'belajar',  # tambahkan app
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

Lalu tambahkan konfigurasi SPECTACULAR_SETTINGS (optional):

```py
SPECTACULAR_SETTINGS = {
    'TITLE': 'Belajar DRF API',
    'DESCRIPTION': 'API sederhana untuk belajar DRF CBV',
    'VERSION': '1.0.0',
}

```

#### 2.4 URL utama (myproject/urls.py)

```py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('belajar.urls')),  # include url dari app belajar
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # openapi schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger ui
]

```

#### 2.5 URL App (belajar/urls.py)

```py
# belajar/urls.py
from django.urls import path
from .views import HaloView, NamaView

urlpatterns = [
    path('halo', HaloView.as_view(), name='halo'), # URL untuk endpoint halo
    path('nama/<str:nama>', NamaView.as_view(), name='nama'),# URL untuk endpoint nama
]

```

#### 2.6 Serializer In/Out {belajar/serializers.py}

```py
# belajar/serializers.py
from rest_framework import serializers
#Serializer untuk input Halo
class HaloInputSerializer(serializers.Serializer):
    nama = serializers.CharField()
    alamat = serializers.CharField()

#Serializer Input dan Output untuk Message
class MessageResponseSerializer(serializers.Serializer):
    message = serializers.CharField()

```

#### 2.7 Views Apps CBV (belajar/views.py)

Tapi di Django, kalau method GET dan POST endpoint-nya sama (/halo), lebih baik gabung dalam satu view. Jadi kita perbaiki nanti di views.py.

```py
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


```

Migrasi dan Jalankan Server

```cmd
python manage.py migrate
python manage.py runserver
```

#### 2.8 Unit Test (belajar/test.py) pakai pytest-drf

```py
# pytest.ini sejajar dengan manage.py
[pytest]
DJANGO_SETTINGS_MODULE = myproject.settings #Folder utama.settings
python_files = tests.py test_*.py *_tests.py
```

```py
# belajar/tests.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestHaloView:
    def test_get_halo(self, api_client):
        url = reverse('halo')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"message": "Belajar DRF CBV"}
    
    def test_post_halo_valid_data(self, api_client):
        url = reverse('halo')
        data = {
            "nama": "Silmi",
            "alamat": "Semarang"
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data == data
    
    def test_post_halo_invalid_data(self, api_client):
        url = reverse('halo')
        data = {
            "nama": "",  # invalid - empty string
            "alamat": "Semarang"
        }
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "nama" in response.data  # error message for nama field
```

Jalankan Test `pytest`

#### 2.9 Unit Test (request.rest) / Postman

### 3. API PRODUCT

Dalam Django REST Framework (DRF), ViewSet adalah class-based view (CBV) tingkat tinggi yang menyederhanakan penulisan endpoint RESTful untuk model, seperti Product. ViewSet secara otomatis menghubungkan method HTTP (GET, POST, PUT, DELETE) dengan method dalam class seperti list, create, retrieve, update, dan destroy.
```
Contoh API: Product
Misal kamu punya model Product dan ingin membuat endpoint seperti:

Endpoint	    HTTP	Method      ViewSet	Fungsi
/products/	    GET	    list	    Mengambil semua produk
/products/	    POST	create	    Menambahkan produk baru
/products/{id}/	GET	    retrieve	Mengambil detail produk tertentu
/products/{id}/	PUT	    update	    Update penuh produk
/products/{id}/	PATCH	partial_update	Update sebagian produk
/products/{id}/	DELETE	destroy	    Menghapus produk

Penjelasan Method di ViewSet
Method	                            Kegunaan
list(self, request)	                Mengembalikan daftar semua objek
create(self, request)	            Membuat objek baru dari data request
retrieve(self, request, pk=None)	Mengambil detail objek tertentu berdasarkan pk
update(self, request, pk=None)	    Melakukan update penuh (PUT) terhadap objek
partial_update(self, request, pk=None)	Update sebagian (PATCH) terhadap objek
destroy(self, request, pk=None)	        Menghapus objek

```

#### 3.1 API SPECS

No | URL | Method | Request Body | Response Body
1 | /products/ | GET | - | List semua produk:[{ "id": 1, "name": "Produk A", "price": 10000.0 }, ...]
2 | /products/ | POST | { "name": "Produk Baru", "price": 15000.0 } | Produk yang baru dibuat:{ "id": 2, "name": "Produk Baru", "price": 15000.0 }
3 | /products/{id}/ | GET | - | Detail produk tertentu:{ "id": 1, "name": "Produk A", "price": 10000.0 }
4 | /products/{id}/ | PUT | { "name": "Produk Update", "price": 20000.0 } | Produk yang sudah diupdate:{ "id": 1, "name": "Produk Update", "price": 20000.0 }
5 | /products/{id}/ | DELETE | - | { "deleted": true }

Field | Keterangan
{id} | ID produk (integer)
Request Body POST & PUT | JSON berisi name dan price
Response Body | JSON berisi data produk (termasuk id)

#### 3.2 Virtual Environment dan Install Django + DRF

```py
# Buat folder project
mkdir belajar-drf
cd belajar-drf

# Buat virtual environment
python -m venv venv

# Aktifkan venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install Django dan Django REST Framework + drf-spectacular(Swagger) + pytest-drf(Testing)
pip install django djangorestframework drf-spectacular pytest-drf

# Start Django project
#django-admin startproject myproject .

# Buat app
#python manage.py startapp api

```

```py
myproject/
  ├── settings.py
  ├── urls.py
  ├── belajar/
        ├── views.py
        ├── urls.py
        ├── test_belajar.py
  ├── products/
        ├── views.py          # <== Method Request >> Response
        ├── urls.py
        ├── test_products.py
        ├── serializer.py     # <== Validation Request
        ├── service.py        # <== Raw SQL
        ├── schema.py         # <== Documentation Schema
  ├── utils/
        ├── db.py
        ├── response_wrapper.py
        ├── custom_exception.py
```

#### 3.3 Create manual tabel dengan SQL

- DATABASE ORM 

>> jika menggunakan ORM pakailah langkah dibawah

Secara default, Django akan membuat nama tabel di database berdasarkan nama aplikasi dan nama model dengan format:
`<nama_aplikasi>_<nama_model>`

```py
#/siswa/model.py
from django.db import models

class Products(models.Model):
    prod_name = models.CharField(max_length=100)
    price = models.CharField(max_length=15)

    class Meta:
        db_table = "tb_products"  # Menentukan nama tabel di SQLite

```

```py
python3 manage.py makemigrations
python3 manage.py migrate
```

CEK DATA

```py
python manage.py dbshell

.tables
```

- DATABASE NO ORM

>> jika tidak menggunakan ORM pakailah langkah dibawah

```py
python3 manage.py dbshell
```

```sql
-- create tabel
CREATE TABLE tb_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prod_name TEXT NOT NULL,
    price REAL NOT NULL
);



-- mengetahui semua tabel yang ada
.tables 

-- melihat struktur tabel
PRAGMA table_info(tbl_customer); 
```


#### 3.4 Setting Django (myproject/settings.py)

```py

INSTALLED_APPS = [
    ...
    'rest_framework',
    'api',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Belajar DRF API',
    'DESCRIPTION': 'API Documentation for Products',
    'VERSION': '1.0.0',
}

```

#### 3.5 Utils Folder (db.py, custom_exception.py, response_wrapper.py )

response_wrapper.py

```py
def success_response(data):
    return {
        "status": "success",
        "data": data
    }

```

custom_exception.py

```py
from rest_framework.exceptions import APIException

class NotFoundException(APIException):
    status_code = 404
    default_detail = 'Not found.'
    default_code = 'not_found'

```

db.py

```py
from django.db import connection

from contextlib import contextmanager

@contextmanager
def get_cursor_dict():
    cursor = connection.cursor()
    try:
        yield DictCursor(cursor)
    finally:
        cursor.close()

class DictCursor:
    def __init__(self, cursor):
        self.cursor = cursor

    def execute(self, *args, **kwargs):
        return self.cursor.execute(*args, **kwargs)

    def fetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def fetchone(self):
        row = self.cursor.fetchone()
        if row is None:
            return None
        columns = [col[0] for col in self.cursor.description]
        return dict(zip(columns, row))

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    @property
    def rowcount(self):
        return self.cursor.rowcount

```

#### 3.6 URL utama (myproject/urls.py)

```py
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

```

#### 3.7 URL App (api/urls.py)

```py
from rest_framework.routers import DefaultRouter
from api.views.products_view import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')

urlpatterns = router.urls

```

#### 3.8 Serializer In/Out (api/serializers.py)

```py
from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    price = serializers.FloatField()

```

#### 3.9 Views App CBV (api/views.py)

```py
from rest_framework import viewsets, status
from rest_framework.response import Response
from api.serializers.products_serializer import ProductSerializer
from api.services.products_service import ProductService
from api.utils.response_wrapper import success_response
from api.utils.custom_exception import NotFoundException

from api.schemas.products_schema import (
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
        return Response(success_response(products))

    @product_retrieve_schema
    def retrieve(self, request, pk=None):
        product = ProductService.get_product_by_id(pk)
        if not product:
            raise NotFoundException('Product not found')
        return Response(success_response(product))

    @product_create_schema
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        new_product = ProductService.create_product(data['name'], data['price'])
        return Response(success_response(new_product), status=status.HTTP_201_CREATED)

    @product_update_schema
    def update(self, request, pk=None):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        updated_product = ProductService.update_product(pk, data['name'], data['price'])
        if not updated_product:
            raise NotFoundException('Product not found')
        return Response(success_response(updated_product))

    @product_delete_schema
    def destroy(self, request, pk=None):
        deleted = ProductService.delete_product(pk)
        if not deleted:
            raise NotFoundException('Product not found')
        return Response(success_response({"deleted": True}), status=status.HTTP_204_NO_CONTENT)

```

#### 3.9 Services App CBV (api/views.py)

```py
from api.utils.db import get_cursor_dict

class ProductService:
    @staticmethod
    def get_all_products():
        with get_cursor_dict() as cursor:
            cursor.execute("SELECT * FROM tb_products")
            return cursor.fetchall()

    @staticmethod
    def get_product_by_id(product_id):
        with get_cursor_dict() as cursor:
            cursor.execute("SELECT * FROM tb_products WHERE id = ?", [product_id])
            return cursor.fetchone()

    @staticmethod
    def create_product(name, price):
        with get_cursor_dict() as cursor:
            cursor.execute("INSERT INTO tb_products (name, price) VALUES (?, ?)", [name, price])
            new_id = cursor.lastrowid
            return {"id": new_id, "name": name, "price": price}

    @staticmethod
    def update_product(product_id, name, price):
        with get_cursor_dict() as cursor:
            cursor.execute("UPDATE tb_products SET name = ?, price = ? WHERE id = ?", [name, price, product_id])
            if cursor.rowcount == 0:
                return None
            return {"id": int(product_id), "name": name, "price": price}

    @staticmethod
    def delete_product(product_id):
        with get_cursor_dict() as cursor:
            cursor.execute("DELETE FROM tb_products WHERE id = ?", [product_id])
            return cursor.rowcount > 0

```

#### 3.9 Schema App CBV (api/views.py)

```py
from drf_spectacular.utils import extend_schema, OpenApiExample
from api.serializers.products_serializer import ProductSerializer

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
    responses=ProductSerializer(many=True),
    summary="List all products",
    description="Retrieve a list of all products.",
    examples=[product_example],
)

# Create Product
product_create_schema = extend_schema(
    request=ProductSerializer,
    responses=ProductSerializer,
    summary="Create a new product",
    description="Create a new product with name and price.",
    examples=[product_create_example, product_example],
)

# Retrieve Product
product_retrieve_schema = extend_schema(
    responses=ProductSerializer,
    summary="Retrieve a product by ID",
    description="Retrieve product details by its ID.",
    examples=[product_example],
)

# Update Product
product_update_schema = extend_schema(
    request=ProductSerializer,
    responses=ProductSerializer,
    summary="Update a product by ID",
    description="Update an existing product by its ID.",
    examples=[product_create_example, product_example],
)

# Delete Product
product_delete_schema = extend_schema(
    responses=None,
    summary="Delete a product by ID",
    description="Delete an existing product by its ID."
)

```

#### 3.10 Unit Test (api/test_api.py) pakai pytest-drf

```py
import pytest
from pytest_drf import APIClientFixture, ViewSetTest
from pytest_drf.util import url_for

client = APIClientFixture()

@pytest.mark.django_db
class TestProductViewSet(ViewSetTest):
    client = client

    def test_create_product(self):
        data = {"name": "Produk A", "price": 10000}
        response = self.client.post(url_for('products-list'), data, format='json')
        assert response.status_code == 201
        assert response.data['data']['name'] == "Produk A"

    def test_list_products(self):
        response = self.client.get(url_for('products-list'))
        assert response.status_code == 200
        assert 'data' in response.data

    def test_get_product_not_found(self):
        response = self.client.get(url_for('products-detail', pk=9999))
        assert response.status_code == 404

    def test_update_product_not_found(self):
        data = {"name": "Produk X", "price": 20000}
        response = self.client.put(url_for('products-detail', pk=9999), data, format='json')
        assert response.status_code == 404

    def test_delete_product_not_found(self):
        response = self.client.delete(url_for('products-detail', pk=9999))
        assert response.status_code == 404

```

#### 3.11 Unit Test (api/test_api.rest) dengan rest client extension vscode

### 4. AUTH JWT >> login untuk crud api product

### 5. ROLE BASE >> login untuk crud api product + userid

### 6. ONE TO ONE

### 7. ONE TO MANY

### 8. MANY TO MANY

#### 8.1 API SPECS

#### 8.1 API SPECS

#### 8.2 Virtual Environment dan Install Django + DRF

#### 8.3 Create manual tabel dengan SQL

#### 8.4 Setting Django (myproject/settings.py)

#### 8.5 Utils Folder (db.py, custom_exception.py, response_wrapper.py )

#### 8.6 URL utama (myproject/urls.py)

#### 8.7 URL App (api/urls.py)

#### 8.8 Serializer In/Out (api/serializers.py)

#### 8.9 Views App CBV (api/views.py)

#### 8.10 Unit Test (api/test_api.py) pakai pytest-drf

#### 8.11 Unit Test (api/test_api.rest) dengan rest client extension vscode

```

```
