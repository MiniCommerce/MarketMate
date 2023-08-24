from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Cart
from .serializers import CartSerializer
from users.permissions import IsAuthenticated, IsBuyer

class CartView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        buyer = request.user.buyer
        cart_list = Cart.objects.filter(user=buyer)

        if cart_list:
            serializer = CartSerializer(cart_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        buyer = request.user.buyer
        product_id = request.data.get('product_id')
        product = get_object_or_404(product, product_id)

        if product:
            request_data = request.data.copy()
            request_data['user'] = buyer.pk
            request_data['product'] = product.pk
            serializer = CartSerializer(data=request_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        buyer = request.user.buyer
        cart_id = request.data.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)

        if buyer.pk == cart.user_id:
            serializer = CartSerializer(cart, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"status": status.HTTP_401_UNAUTHORIZED})
    
    def delete(self, request):
        buyer = request.user.buyer
        cart_id = request.data.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)

        if buyer.pk == cart.user_id:
            cart.delete()
            return Response({"status": status.HTTP_200_OK})

        return Response({"status": status.HTTP_401_UNAUTHORIZED})