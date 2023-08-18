from django.utils import timezone
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import BuyerSerializer, SellerSerializer


# 구매자 회원 가입
class BuyerRegistrationView(APIView):
    def post(self, request):
        serializer = BuyerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Buyer registered successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 판매자 회원 가입
class SellerRegistrationView(APIView):
    def post(self, request):
        serializer = SellerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Seller registered successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)