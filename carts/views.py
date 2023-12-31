from django.shortcuts import get_object_or_404

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from products.models import Product
from users.models import Buyer
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

            serializer_data = serializer.data.copy()
            for i in range(len(serializer.data)):
                serializer_data[i]['price'] = Product.objects.get(pk=serializer_data[i].get('product')).price
                serializer_data[i]['product'] = Product.objects.get(pk=serializer_data[i].get('product')).product_name
                serializer_data[i]['user'] = Buyer.objects.get(pk=serializer_data[i]['user']).nickname
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error_code':status.HTTP_400_BAD_REQUEST,'error':'장바구니에 물품이 없습니다.'},status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        buyer = request.user.buyer
        product = get_object_or_404(Product, pk=request.data.get("product_id"))
        carts = Cart.objects.filter(user=buyer.pk)

        if carts:
            for cart in carts:
                if product.pk == cart.product.pk:
                    cart.amount += int(request.data.get('amount'))
                    cart.save()
                    return Response({"message": "HTTP_200_OK"}, status=status.HTTP_200_OK)
                else:
                    continue

        request_data = request.data.copy()
        request_data['product'] = product.pk
        request_data['user'] = buyer.pk

        serializer = CartSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'error_code':status.HTTP_406_NOT_ACCEPTABLE, 'error': serializer.errors }, status=status.HTTP_406_NOT_ACCEPTABLE)

    def patch(self, request):
        buyer = request.user.buyer
        cart_id = request.data.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)

        if buyer.pk == cart.user_id:
            serializer = CartSerializer(cart, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response({'error_code':status.HTTP_400_BAD_REQUEST ,'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"error_code": status.HTTP_401_UNAUTHORIZED, 'error':'buyer와 cart의 소유자가 다릅니다.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request):
        buyer = request.user.buyer
        cart_id = request.data.get('cart_id')
        cart = get_object_or_404(Cart, pk=cart_id)

        if buyer.pk == cart.user_id:
            cart.delete()
            return Response({"status": status.HTTP_200_OK})

        return Response({"error_code": status.HTTP_401_UNAUTHORIZED, 'error':'buyer와 cart의 소유자가 다릅니다.'},status=status.HTTP_401_UNAUTHORIZED)