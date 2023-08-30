from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.env import config
from products.models import Product
from products.serializers import ProductSerializer
from carts.models import Cart
from users.permissions import IsAuthenticated, IsBuyer
from .models import Order, Purchase, Item
from .serializers import OrderSerializer, PurchaseSerializer, ItemSerializer

import requests
import json


# Create your views here.
def getToken():
    url = 'https://api.iamport.kr/users/getToken'

    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        'imp_key': config('IMP_KEY', default=None), # REST API Key
        'imp_secret': config('IMP_SECRET', default=None) # REST API Secret
    }

    try:
        response = json.loads(requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t")).text)['response']['access_token']
        return response
    except Exception as ex:
        return ex

def preparePayments(token, merchant_uid, price):
    url = "https://api.iamport.kr/payments/prepare"

    headers = {'Authorization': token, 'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    body = {
        'merchant_uid': merchant_uid,
        'amount': price
    }

    try:
        response = json.loads(requests.post(url, headers=headers, data=json.dumps(body, ensure_ascii=False, indent="\t")).text)['response']
        return response
    except Exception as ex:
        return ex


class OrderView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        order = get_object_or_404(Order, pk=request.GET.get('order_id'))

        serializer = OrderSerializer(order)
        serializer_data = serializer.data.copy()
        serializer_data['buyer_name'] = order.buyer.nickname
        serializer_data['buyer_email'] = order.buyer.email
        serializer_data['buyer_phone'] = order.buyer.number

        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request):
        request_data = request.data.copy()

        buyer = request.user.buyer
        product = get_object_or_404(Product, pk=request_data.pop('product_id'))
        quantity = int(request_data.pop("quantity"))

        request_data['buyer'] = buyer.pk
        request_data['order_name'] = f"{product.product_name} {quantity}건"
        request_data['status'] = 'ready'
        request_data['address'] = buyer.shipping_address
        request_data['price'] = product.price * quantity
        
        order_serializer = OrderSerializer(data=request_data)
        if order_serializer.is_valid():
            order_serializer.save()

            order_data = {}
            order_data['order'] = order_serializer.data.get('id')
            order_data['product'] = product.pk
            order_data['quantity'] = quantity

            item_serializer = ItemSerializer(data=order_data)
            if item_serializer.is_valid():
                item_serializer.save()
                return Response({'order': order_serializer.data, 'item': item_serializer.data}, status=status.HTTP_200_OK)

            return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class CartOrderView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        request_data = request.data.copy()

        buyer = request.user.buyer
        
        carts = []
        for pair in request_data:
            carts.append(Cart.objects.get(pk=pair.get('cart_id')))

        if len(carts) > 1:
            order_name = f'{carts[0].product.product_name} 외 {len(carts) - 1}건'
        else:
            order_name = f'{carts[0].product.product_name} 1건'


        price = 0
        for cart in carts:
            price += ((cart.product.price) * (cart.amount))

        order_data = {}
        order_data['buyer'] = buyer.pk
        order_data['order_name'] = order_name
        order_data['status'] = 'ready'
        order_data['address'] = buyer.shipping_address
        order_data['price'] = price

        order_serializer = OrderSerializer(data=order_data)
        if order_serializer.is_valid():
            order_serializer.save()

            order = Order.objects.get(pk=order_serializer.data.get('id')).pk
            item_data = {}
            for cart in carts:
                item_data['order'] = order
                item_data['product'] = cart.product.pk
                item_data['quantity'] = cart.amount
                
                item_serializer = ItemSerializer(data=item_data)
                if item_serializer.is_valid():
                    item_serializer.save()

            return Response({'order': order_serializer.data, 'item': item_serializer.data}, status=status.HTTP_200_OK)

        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrepurchaseView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        token = getToken()

        res = preparePayments(token, request.data.get('merchant_uid'), request.data.get('price'))
        merchant_uid = res['merchant_uid']
        price = res['amount']

        order = get_object_or_404(Order, pk=request.data.get('order_id'))
        buyer = request.user.buyer

        items = Item.objects.filter(order=order.pk)
        for item in items:
            if item.quantity > item.product.amount:
                return Response({"message": "재고보다 주문량이 많습니다."})

        if buyer and (merchant_uid == request.data.get('merchant_uid')) and (order.price == price):
            request_data = request.data.copy()
            request_data['order'] = order.pk
            request_data['buyer'] = buyer.pk
            request_data['status'] = 'ready'
            request_data['price'] = price

            serializer = PurchaseSerializer(data=request_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostpurchaseView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def patch(self, request):
        request_data = request.data.copy()

        purchase = get_object_or_404(Purchase, merchant_uid=request_data.pop("merchant_uid"))
        order = Order.objects.get(pk=request_data.get("order_id"))
        items = Item.objects.filter(order=request_data.pop("order_id"))

        for item in items:
            item.product.amount -= item.quantity
            item.product.save()
        
        order.status = request_data.get("status")
        order.save()

        serializer = PurchaseSerializer(purchase, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


def performRefund(token, imp_uid, amount):
    url = f"https://api.iamport.kr/payments/cancel"
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    
    data = {
        'imp_uid': imp_uid,
        'amount': amount
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response_data = response.json()
        
        if response_data['code'] == 0:
            return 'success'
        else:
            return 'failed'
    except Exception as ex:
        return 'failed'


# 환불
class RefundView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        purchase = get_object_or_404(Purchase, merchant_uid=request.data.get('merchant_uid'))

        if purchase.status != 'refunded':
            token = getToken()

            # 환불 로직 추가
            refund_result = performRefund(token, purchase.imp_uid, purchase.price)
            if refund_result == 'success':
                # 환불 처리 성공 시 업데이트
                purchase.status = 'refunded'
                purchase.save()

                # 주문 및 상품 업데이트 로직 추가
                order = purchase.order
                order.status = 'refunded'
                order.save()

                product = order.product
                product.amount += 1
                product.save()

                return Response({'message': 'Refund successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Refund failed'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Already refunded'}, status=status.HTTP_400_BAD_REQUEST)
        

# 주문 조회
class BuyerOrdersView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def get(self, request):
        buyer = request.user.buyer
        orders = Order.objects.filter(buyer=buyer)
        serializer = OrderSerializer(orders, many=True)

        orders_with_images = []
        for order_data in serializer.data:
            order_id = order_data['id']
            product_id = order_data['product']

            try:
                product = Product.objects.get(pk=product_id)
                product_images = product.images.all()  
                product_images_urls = [image.image.url for image in product_images]

                order_data['product_images'] = product_images_urls
                orders_with_images.append(order_data)
            except Product.DoesNotExist:
                pass

        return Response(orders_with_images, status=status.HTTP_200_OK)