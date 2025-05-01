## TEKNOLOGI YANG DIPELAJARI DRF CBV
- venv >> virtual environtment
- Default Router >> list,create,update,destroy
- Serializer Input dan Output >> validation
- APIView >> req-validation-proses-response
- async function, try except >> get API from others
- Services >> Raw SQL Operation
- Utils >> db.py, response wrapper, custom exception 
- drf-spectacular >> extend schema >> schema open api documentation
- pytest-django >> unit test terstruktur
- docker >> deploy server
- auth >> jwt
- role base >> user
- sql realation >> one to one, one to many, many to many
- sql atomic and rollback
- nosql database
- postgree database



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

# Install Django dan Django REST Framework + drf-spectacular(Swagger) + pytest-django(Testing)
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

Ketika kamu menggunakan DefaultRouter, nama-nama URL akan otomatis dibuat berdasarkan pola:
router.register('product', ProductViewSet, basename='product-url')

Nama untuk endpoint list adalah: 'product-url-list'
Nama untuk endpoint detail adalah: 'product-url-detail'
url = reverse('product-url-list') >> auto definde pada reverse

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

# Install Django dan Django REST Framework + drf-spectacular(Swagger) + pytest-django(Testing)
pip install django djangorestframework pytest pytest-django drf-spectacular

# Start Django project
#django-admin startproject myproject .

# Buat app
python manage.py startapp products

```

```py
myproject/
  ├── settings.py
  ├── urls.py
  ├── utils/
        ├── db.py
        ├── response_wrapper.py
        ├── custom_exception.py
  ├── belajar/
        ├── views.py
        ├── urls.py
        ├── tests.py
  ├── productss/
        ├── views.py          # <== Method Request >> Response
        ├── urls.py
        ├── tests.py
        ├── serializer.py     # <== Validation Request
        ├── service.py        # <== Raw SQL
        ├── schema.py         # <== Documentation Schema
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
CTRL + D >> keluar dari dbshell

#### 3.4 Setting Django (myproject/settings.py)

```py

INSTALLED_APPS = [
    ...
    'product',
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
def success_response(message=None, data=None, status="success"):
    return {
        "status": status,
        "message": message,
        "data": data if data is not None else {}
    }

```

custom_exception.py

```py
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from myproject.utils.response_wrapper import success_response

class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found'
    default_code = 'not_found'

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is not None:
        response.data = success_response(status='error', data=None, message=str(exc))
    return response

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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('belajar.urls')),  # include url dari app belajar
    path('', include('product.urls')),  # include url dari app products
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # openapi schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger ui
]


```

#### 3.7 URL App (api/urls.py)

```py
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet


router = DefaultRouter()
router.register('product', ProductViewSet, basename='product-url')

urlpatterns = router.urls

```

#### 3.8 Serializer In/Out (api/serializers.py)

```py
#/product/serializer.py >>validation dan swagger input
from rest_framework import serializers

class ProductInputSerializer(serializers.Serializer):
    prod_name = serializers.CharField()
    price = serializers.FloatField()

class ProductOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    prod_name = serializers.CharField()
    price = serializers.FloatField()

```


#### 3.9 Membuat Response yang mudah

GET /product >> data statid
```json
{
  "status": "success",
  "message": "GET ALL PRODUCTS",
  "data": [
    {
      "id": 1,
      "prod_name": "Product 1",
      "price": 10
    },
    {
      "id": 2,
      "prod_name": "Product 2",
      "price": 20
    }
  ]
}
```
Mari Kita Implementasikan :

```py 
#### serializer.py >> tentukan input req dan output res >> lihat atas

#### views.py >> buat req response sederhana seperti api specs
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


#### urls.py Utama >> register urls product >> lihat atas
#### urls.py product >> rambil views >> lihat atas

#### schemas.py >> documentation
#product/schemas.py
from drf_spectacular.utils import extend_schema, OpenApiExample
from product.serializers import ProductOutputSerializer

# Example Object (bisa reusable)
product_example = OpenApiExample(
    'Product Example',
    value={
        "id": 1,
        "prod_name": "Produk Contoh",
        "price": 10000.0
    },
    request_only=False,  # tampil di response
    response_only=False, # tampil di request
)

# List Products
product_list_schema = extend_schema(
    responses=ProductOutputSerializer(many=True),
    summary="List all products",
    description="Retrieve a list of all products.",
    examples=[product_example],
)

#### unit test product
# product/tests.py
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
class TestProductView:
    def test_get_all_products(self, api_client):
        # Insert data jika sql nanti

        url = reverse('product-url-list')  # pastikan ini sesuai dengan nama path di urls.py
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = response.data

        assert data["status"] == "success"
        assert data["message"] == "GET ALL PRODUCTS"
        #assert "products" in data["data"]
        #assert len(data["data"]["products"]) == 2
        assert len(data["data"]) == 2
        print(data)

        #names = [p["name"] for p in data["data"]["products"]]
        names = [p["prod_name"] for p in data["data"]]
        assert "Product 1" in names
        assert "Product 2" in names
    

#Jalankan test
pytest product

#Jalankan server
pyhton manage.py runserver

#API DOCS
http://127.0.0.1:8000/docs/

#DJANGO REST
http://127.0.0.1:8000/product/
```
=======================================================================
bracnh 02_product >> melanjutkan api product dengan sqlite

Catatan Penting : 
- SQL pada django >> `cursor.execute("SELECT * FROM tb_products WHERE id = %s", [pk])`
- Pada unit pytest >> def create_test_table(django_db_setup, django_db_blocker): sebelum seup

#### 3.9 create product Views App CBV (api/views.py)

#### 3.9 Views App CBV (api/views.py)

```py
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

```

#### 3.9 Services App CBV (api/views.py)

```py
#product/services.py
from myproject.utils.db import get_cursor_dict


class ProductService:
    @staticmethod
    def get_all_products():
        with get_cursor_dict() as cursor:
            cursor.execute("SELECT * FROM tb_products")
            return cursor.fetchall()

    @staticmethod
    def get_product_by_id(product_id):
        with get_cursor_dict() as cursor:
            cursor.execute("SELECT * FROM tb_products WHERE id = %s", [product_id])
            return cursor.fetchone()

    @staticmethod
    def create_product(prod_name, price):
        with get_cursor_dict() as cursor:
            cursor.execute("INSERT INTO tb_products (prod_name, price) VALUES (%s, %s)", [prod_name, price])
            new_id = cursor.lastrowid
            return {"id": new_id, "prod_name": prod_name, "price": price}

    @staticmethod
    def update_product(product_id, prod_name, price):
        with get_cursor_dict() as cursor:
            cursor.execute("UPDATE tb_products SET prod_name = %s, price = %s WHERE id = %s", [prod_name, price, product_id])
            if cursor.rowcount == 0:
                return None
            return {"id": int(product_id), "prod_name": prod_name, "price": price}

    @staticmethod
    def delete_product(product_id):
        with get_cursor_dict() as cursor:
            cursor.execute("DELETE FROM tb_products WHERE id = %s", [product_id])
            return cursor.rowcount > 0

```

#### 3.9 Schema App CBV (api/views.py)

```py
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

```

#### 3.10 Unit Test (api/test_api.py) pakai pytest-drf

```py
# product/tests.py
from django.db import connection
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

# === Fixtures ===
@pytest.fixture(scope="session", autouse=True)
def create_test_table(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prod_name TEXT NOT NULL,
                    price REAL NOT NULL
                )
            """)

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_products():
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO tb_products ( prod_name, price) VALUES ('macbook', 100)")
        cursor.execute("INSERT INTO tb_products ( prod_name, price) VALUES ('surface', 200)")
    yield
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM tb_products")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='tb_products'")  # reset autoincrement
        

# === Test Class ===
@pytest.mark.django_db
class TestProductView:

    def test_get_all_products(self, api_client, setup_products):
        url = reverse('product-url-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["status"] == "success"
        names = [p["prod_name"] for p in response.data["data"]]
        assert "macbook" in names and "surface" in names

    def test_get_single_product(self, api_client, setup_products):
        url = reverse('product-url-detail', args=[1])
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["prod_name"] == "macbook"

    def test_create_product(self, api_client):
        url = reverse('product-url-list')
        payload = {"prod_name": "New Product", "price": 15.5}
        response = api_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["data"]["prod_name"] == "New Product"

    def test_update_product(self, api_client, setup_products):
        url = reverse('product-url-detail', args=[1])
        payload = {"prod_name": "Updated Product", "price": 99.9}
        response = api_client.put(url, data=payload, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["data"]["prod_name"] == "Updated Product"

    def test_delete_product(self, api_client, setup_products):
        url = reverse('product-url-detail', args=[1])
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_create_product_invalid_name(self, api_client):
        url = reverse('product-url-list')
        payload = {"prod_name": "", "price": 10.0}
        response = api_client.post(url, data=payload, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "prod_name" in response.data

```

#### 3.11 Unit Test (api/test_api.rest) dengan rest client extension vscode

### 4. AUTH JWT >> login untuk crud api product

```py
pip install djangorestframework-simplejwt
python manage.py migrate
python manage.py runserver

#buat folder auth
```
#### 1. settings.py

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_spectacular',
    'belajar',  # tambahkan app
    'product',  # tambahkan app
    'rest_framework_simplejwt', #auth jwt
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'TEST_REQUEST_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```
#### 2. serializers

```py
#auth/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

class UpdatePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, min_length=6)

class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
```

#### 3. schema

```py
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, OpenApiParameter
from auth.serializers import (
    RegisterSerializer,
    UpdatePasswordSerializer,
    UserOutputSerializer
)

register_schema = extend_schema(
    request=RegisterSerializer,
    responses={201: UserOutputSerializer},
    examples=[
        OpenApiExample(
            "Register Example",
            value={"username": "user1", "password": "123456"},
        )
    ],
    description="Register a new user.",
)

update_password_schema = extend_schema(
    request=UpdatePasswordSerializer,
    responses={200: OpenApiResponse(description="Password updated")},
    examples=[
        OpenApiExample(
            "Update Password Example",
            value={"new_password": "newpass123"},
        )
    ],
    description="Update password. Requires authentication.",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            type=str,
            location=OpenApiParameter.HEADER,
            required=True,
            description='JWT access token. Format: Bearer <access_token>'
        )
    ]
)

logout_schema = extend_schema(
    responses={200: OpenApiResponse(description="Logout successful")},
    description="Logout current user. Requires authentication.",
    parameters=[
        OpenApiParameter(
            name='Authorization',
            type=str,
            location=OpenApiParameter.HEADER,
            required=True,
            description='JWT access token. Format: Bearer <access_token>'
        )
    ]
)

```

#### 4. views

```py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from auth.serializers import (
    RegisterSerializer,
    UpdatePasswordSerializer,
    UserOutputSerializer
)
from auth.schemas import register_schema, update_password_schema, logout_schema


class RegisterView(APIView):
    @register_schema
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )
            return Response(UserOutputSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    @logout_schema
    def post(self, request):
        return Response({"message": "Logout successful"}, status=200)

class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @update_password_schema
    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data["new_password"])
            request.user.save()
            return Response({"message": "Password updated"}, status=200)
        return Response(serializer.errors, status=400)


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
from rest_framework.permissions import IsAuthenticated

class ProductViewSet(viewsets.ViewSet):
    
    permission_classes = [IsAuthenticated]

    @product_list_schema
    def list(self, request):
        products = ProductService.get_all_products()
        return Response(success_response("GET ALL PRODUCTS",products))


```

#### 5. urls >> auth

```py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from auth.views import LogoutView, RegisterView, UpdatePasswordView


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("update-password/", UpdatePasswordView.as_view(), name="update_password"),
]

```

#### 6. urls >> utama (myapps)

```py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('belajar.urls')),  # include url dari app belajar
    path('', include('product.urls')),  # include url dari app products
    path('auth/', include('auth.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),  # openapi schema
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # swagger ui
]
```

#### 7. tests.py

```py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

client = APIClient()

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User

client = APIClient()

@pytest.mark.django_db
def test_register_user():
    response = client.post(reverse("register"), {"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    assert response.data["username"] == "testuser"

@pytest.mark.django_db
def test_login_user():
    User.objects.create_user(username="testuser", password="testpass")
    response = client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_update_password():
    user = User.objects.create_user(username="testuser", password="testpass")
    login = client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "testpass"})
    token = login.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.post(reverse("update_password"), {"new_password": "newpass123"})
    assert response.status_code == 200
    assert response.data["message"] == "Password updated"

    # Test login with new password
    client.credentials()  # clear token
    login2 = client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "newpass123"})
    assert login2.status_code == 200
    assert "access" in login2.data

@pytest.mark.django_db
def test_logout_user():
    user = User.objects.create_user(username="testuser", password="testpass")
    login = client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "testpass"})
    token = login.data["access"]

    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    response = client.post(reverse("logout"))
    assert response.status_code == 200
    assert response.data["message"] == "Logout successful"

@pytest.mark.django_db
def test_login_wrong_password():
    User.objects.create_user(username="testuser", password="testpass")
    response = client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401
    assert "access" not in response.data

# @pytest.mark.django_db
# def test_protected_product_access():
#     user = User.objects.create_user(username="testuser", password="testpass")
#     login = client.post(reverse("token_obtain_pair"), {"username": "testuser", "password": "testpass"})
#     token = login.data["access"]
#     client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

#     url = reverse("product-list")  # pastikan pakai nama URL yang sesuai
#     response = client.get(url)
#     assert response.status_code == 200

```


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
