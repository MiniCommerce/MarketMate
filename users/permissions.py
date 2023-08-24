from rest_framework.permissions import BasePermission

from users.models import Seller, Buyer


class IsAuthenticated(BasePermission):
    '''
    Token 유무로 API요청 제한
    '''

    def has_permission(self, request, view):
        return bool(request.user and request.auth)


class IsSeller(BasePermission):
    '''
    Seller만 API요청 받기
    '''

    def has_permission(self, request, view):
        user_id = request.user.id

        try:
            seller = Seller.objects.get(pk=user_id)
            return True
        except Seller.DoesNotExist:
            return False


class IsBuyer(BasePermission):
    '''
    Buyer만 API요청 받기
    '''

    def has_permission(self, request, view):
        user_id = request.user.id

        try:
            seller = Buyer.objects.get(pk=user_id)
            return True
        except Buyer.DoesNotExist:
            return False