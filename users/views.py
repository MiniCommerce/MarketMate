from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication

from .serializers import BuyerSerializer, SellerSerializer, LoginSerializer, ChangePasswordSerializer, BuyerUpdateSerializer, SellerUpdateSerializer, DeleteUserSerializer
from users.permissions import IsAuthenticated, IsBuyer, IsSeller


# 판매자 회원가입
class BuyerRegistrationView(APIView):
    def post(self, request):
        serializer = BuyerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Buyer registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({
                'error_code': status.HTTP_400_BAD_REQUEST,
                'error': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST)


# 구매자 회원가입
class SellerRegistrationView(APIView):
    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Seller registered successfully'}, status=status.HTTP_201_CREATED)
        
        return Response({
                'error_code': status.HTTP_400_BAD_REQUEST,
                'error': serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            data = {
                'token': serializer.validated_data['token'].key,
                'user_id': serializer.validated_data['user_id'],
                'member': serializer.validated_data['member']
            }
           
            return Response(data, status=status.HTTP_200_OK)
        
        return Response({
                'error_code': status.HTTP_401_UNAUTHORIZED,
                'error': '유효하지 않는 유저정보 입니다.'
                },
                status=status.HTTP_401_UNAUTHORIZED)


# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        try:
            Token.objects.get(user_id=user.id).delete()
        except Token.DoesNotExist:
            return Response({
                'error_code': status.HTTP_404_NOT_FOUND,
                'error': '유효하지 않는 유저정보 입니다.'
                }, 
                status=status.HTTP_404_NOT_FOUND)
        
        return Response({'status':200},status=status.HTTP_200_OK)


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
                return Response({'message': '비밀번호 변경 성공','status':200 },status=status.HTTP_200_OK)
            else:
                return Response({
                    'error_code': status.HTTP_400_BAD_REQUEST,
                    'error': '현재 암호가 틀립니다.'
                    },
                    status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'error_code': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST)
    

# 구매자 회원정보 수정
class BuyerUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        buyer = request.user.buyer
        serializer = BuyerUpdateSerializer(buyer)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        buyer = request.user.buyer
        serializer = BuyerUpdateSerializer(buyer, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({
            'error_code': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST)
    

# 판매자 회원정보수정
class SellerUpdateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        seller = request.user.seller
        serializer = SellerUpdateSerializer(seller)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        seller = request.user.seller
        serializer = SellerUpdateSerializer(seller, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({
            'error_code': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)
    

# 회원탈퇴
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

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
                    return Response({'status':200}, status=status.HTTP_200_OK)
                except Token.DoesNotExist:
                    return Response({
                        'error_code': status.HTTP_404_NOT_FOUND,
                        'error': '유효하지 않는 유저정보 입니다.'
                        },
                        status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'error_code': status.HTTP_401_UNAUTHORIZED,
            'error': '유효하지 않는 유저정보 입니다.'
            },
            status=status.HTTP_401_UNAUTHORIZED)


# 판매자, 구매자 판별 
class DiscriminationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get(self, request):
        user = request.user

        if user.is_authenticated:
            if hasattr(user, 'seller'):
                return Response({'message': '판매자', 'user_id': user.id})
            elif hasattr(user, 'buyer'):
                return Response({'message': '구매자', 'user_id': user.id})
            else:
                return Response({
                        'error_code': status.HTTP_401_UNAUTHORIZED,
                        'error': '유효하지 않는 유저정보 입니다.'
                        },
                        status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error_code': status.HTTP_401_UNAUTHORIZED,
                'error': '로그인되지 않았습니다.'
                }, 
                status=status.HTTP_401_UNAUTHORIZED)