from django.urls import path
from .views import BuyerRegistrationView, SellerRegistrationView

app_name = 'users'

urlpatterns = [
    path('buyer/signin/', BuyerRegistrationView.as_view(), name='buyer-signin'),
    path('seller/signin/', SellerRegistrationView.as_view(), name='seller-signin'),
    # 다른 URL 패턴들을 여기에 추가할 수 있습니다.
]
