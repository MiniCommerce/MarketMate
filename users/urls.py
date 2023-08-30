from django.urls import path
from .views import BuyerRegistrationView, SellerRegistrationView, LoginView, LogoutView, ChangePasswordView, BuyerUpdateView, SellerUpdateView, DeleteUserView, DiscriminationView

app_name = 'users'

urlpatterns = [
    # 구매자 회원가입
    path('buyer/signin/', BuyerRegistrationView.as_view(), name='buyer-signin'),
    # 판매자 회원가입
    path('seller/signin/', SellerRegistrationView.as_view(), name='seller-signin'),
    # 로그인
    path('login/', LoginView.as_view(), name='login'),
    # 로그아웃
    path('logout/', LogoutView.as_view(), name='logout'),
    # 비밀번호 변경
    path('changepw/', ChangePasswordView.as_view(), name='changepw'),
    # 구매자 정보 수정
    path('buyer/update/', BuyerUpdateView.as_view(), name='buyerupdate'),
    # 판매자 정보 수정
    path('seller/update/', SellerUpdateView.as_view(), name='sellerupdate'),
    # 회원탈퇴
    path('delete/', DeleteUserView.as_view(), name='delete_user'),
    # 구매자, 판매자 식별
    path('discrimination/', DiscriminationView.as_view(), name='discriminationuser')
]
