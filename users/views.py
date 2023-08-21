from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .serializers import BuyerSerializer, SellerSerializer, LoginSerializer, ChangePasswordSerializer, BuyerUpdateSerializer, SellerUpdateSerializer, DeleteUserSerializer
from users.permissions import IsAuthenticated


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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        try:
            Token.objects.get(user_id=user.id).delete()
        except Token.DoesNotExist:
            return Response({'message': '유효하지 않는 유저정보 입니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(status=status.HTTP_200_OK)


# 비밀번호 변경
class ChangePasswordView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            current_password = serializer.validated_data.get('current_password')
            new_password = serializer.validated_data.get('new_password')
            
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': '비밀번호 변경 성공'})
            else:
                return Response({'error': '현재 암호가 틀립니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 구매자 회원정보 수정
class BuyerUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        buyer = request.user.buyer
        serializer = BuyerUpdateSerializer(buyer)
        
        return Response(serializer.data)

    def put(self, request):
        buyer = request.user.buyer
        serializer = BuyerUpdateSerializer(buyer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 판매자 회원정보수정
class SellerUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller = request.user.seller
        serializer = SellerUpdateSerializer(seller)

        return Response(serializer.data)

    def put(self, request):
        seller = request.user.seller
        serializer = SellerUpdateSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 회원탈퇴
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = DeleteUserSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            if user.check_password(password):
                try:
                    Token.objects.get(user_id=user.id).delete()
                    user.is_active = False
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                except Token.DoesNotExist:
                    return Response({'message': '유효하지 않는 유저정보 입니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'message': '유효하지 않는 유저정보 입니다.'}, status=status.HTTP_401_UNAUTHORIZED)