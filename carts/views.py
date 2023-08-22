from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import Buyer
from products.models import Product
from .models import Cart
from .serializers import CartSerializer


# Create your views here.
class CartView(APIView):
    def get(self, request):
        user = get_object_or_404(Buyer, pk=Token.objects.get(key=request.auth).user_id)
        cart_list = Cart.objects.filter(user=user)

        if cart_list:
            serializer = CartSerializer(cart_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = get_object_or_404(Buyer, pk=Token.objects.get(key=request.auth).user_id)
        product = Product.objects.get(pk=request.data.get('product_id'))

        if user and product:
            request_data = request.data.copy()
            request_data['user'] = user.pk
            request_data['product'] = product.pk
            serializer = CartSerializer(data=request_data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"status": status.HTTP_401_UNAUTHORIZED})

    def patch(self, request):
        user = get_object_or_404(Buyer, pk=Token.objects.get(key=request.auth).user_id)
        cart = Cart.objects.get(pk=request.data.get('cart_id'))

        if user.pk == cart.user_id:
            serializer = CartSerializer(cart, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"status": status.HTTP_401_UNAUTHORIZED})
    
    def delete(self, request):
        user = get_object_or_404(Buyer, pk=Token.objects.get(key=request.auth).user_id)
        cart = Cart.objects.get(pk=request.data.get('cart_id'))

        if user.pk == cart.user_id:
            cart.delete()
            return Response({"status": status.HTTP_200_OK})

        return Response({"status": status.HTTP_401_UNAUTHORIZED})