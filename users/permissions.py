from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    '''
    Token 유무로 API요청 제한
    '''

    def has_permission(self, request, view):
        return bool(request.user and request.auth)