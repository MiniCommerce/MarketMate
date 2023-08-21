from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import BuyerSerializer, SellerSerializer, LoginSerializer


# 판매자 회원가입
class BuyerRegistrationView(APIView):
    def post(self, request):
        serializer = BuyerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Buyer registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 구매자 회원가입
class SellerRegistrationView(APIView):
    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Seller registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            token = serializer.validated_data
            
            return Response({
                'token': token.key,
            }, status=status.HTTP_200_OK)
        
        return Response({'message': '유효하지 않는 유저정보 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)


# 로그아웃
class LogoutView(APIView):
    def get(self, request):
        user = request.user
        
        try:
            Token.objects.get(user_id=user.id).delete()
        except Token.DoesNotExist:
            return Response({'message': '유효하지 않는 유저정보 입니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_200_OK)