from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("list/", views.ProductList.as_view(), name="상품 목록 조회"),
    path("register/", views.ProductCreateView.as_view(), name="상품 등록"),
    path("detail/", views.ProductDetail.as_view(), name="상품 상세정보 조회"),
    path("update/", views.ProductDetail.as_view(), name="상품 정보 수정"),
]