from django.urls import path
from .views import BuyerRegistrationView, SellerRegistrationView, Login

app_name = 'users'

urlpatterns = [
    # 구매자 회원가입
    path('buyer/signin/', BuyerRegistrationView.as_view(), name='buyer-signin'),
    # 판매자 회원가입
    path('seller/signin/', SellerRegistrationView.as_view(), name='seller-signin'),
    # 로그인
    path('login/', Login.as_view(), name='login'),
]
