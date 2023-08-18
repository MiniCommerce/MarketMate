from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Cart
from .serializers import CartSerializer


# Create your views here.
class CartView(APIView):
    def get(self, request):
        cart = Cart.objects.filter(user=request.user)
        
        if not cart:
            return Response({"message": "장바구니가 비었습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartSerializer(cart, many=True)

        if serializer:
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"message": "오류가 발생했습니다."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        serializer = CartSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        cart = Cart.objects.filter(user=request.user, id=request.data["cart_id"]).first()
        serializer = CartSerializer(cart, data={"amount": request.data["amount"]}, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)
