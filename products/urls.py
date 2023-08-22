from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.ProductList.as_view(), name="상품 목록 조회"),
    path("register/", views.ProductList.as_view(), name="상품 등록")
]