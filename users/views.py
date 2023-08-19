from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

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
class Login(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user:
            login(request, user)
            return Response({'message': '로그인 성공'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': '이메일 또는 비밀번호가 잘못되었습니다.'}, status=status.HTTP_401_UNAUTHORIZED)


# 로그인(토큰)
class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        token = serializer.validated_data
        return Response({
            'token': token.key,
        }, status=status.HTTP_200_OK)