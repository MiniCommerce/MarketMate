from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from main.env import config
from products.models import Product
from products.serializers import ProductSerializer
from users.permissions import IsAuthenticated, IsBuyer
from .models import Order, Purchase
from .serializers import OrderSerializer, PurchaseSerializer

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
        order = get_object_or_404(Order, pk=request.data.get('order_id'))
        product = get_object_or_404(Product, pk=order.product.pk)

        serializer = OrderSerializer(order)
        serializer_data = serializer.data.copy()
        serializer_data['product'] = product.product_name
        serializer_data['buyer_name'] = order.buyer.nickname
        serializer_data['buyer_email'] = order.buyer.email
        serializer_data['buyer_phone'] = order.buyer.number
        serializer_data['address'] = order.address
        serializer_data['seller'] = product.seller.store_name
        serializer_data['order_name'] = order.order_name
        serializer_data['status'] = order.status
        serializer_data['price'] = order.price

        return Response(serializer_data, status=status.HTTP_200_OK)

    def post(self, request):
        product = get_object_or_404(Product, pk=request.data.get('product_id'))

        request_data = request.data.copy()
        request_data['product'] = product.pk
        request_data['buyer'] = request.user.buyer.pk
        request_data['seller'] = product.seller.pk
        request_data['order_name'] = f'{product.product_name} 1건'
        request_data['status'] = 'ready'
        request_data['address'] = request.user.buyer.shipping_address
        request_data['price'] = product.price
        
        serializer = OrderSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrepurchaseView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        order = get_object_or_404(Order, pk=request.data.get('order_id'))

        token = getToken()

        res = preparePayments(token, request.data.get('merchant_uid'), order.price)
        merchant_uid = res['merchant_uid']
        price = res['amount']


        request_data = request.data.copy()
        request_data['order'] = order.pk
        request_data['buyer'] = request.user.buyer.pk
        request_data['status'] = 'ready'
        request_data['price'] = price

        serializer = PurchaseSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'api_token': token, 'merchat_uid': merchant_uid, 'price': price, 'status': serializer.data.get('status')}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostpurchaseView(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def put(self, request):
        purchase = get_object_or_404(Purchase, merchant_uid=request.data.get('merchant_uid'))
        order = get_object_or_404(Order, pk=purchase.order.pk)
        product = get_object_or_404(Product, pk=order.product.pk)

        purchase_update_data = {
            'imp_uid': request.data.get('imp_uid'),
            'status': request.data.get('status')
        }
        order_update_data = {
            'status': request.data.get('status')
        }
        product_update_data = {
            'amount': product.amount - 1
        }
        
        if purchase.price == int(request.data.get('price')):
            purchase_serializer = PurchaseSerializer(purchase, data=purchase_update_data, partial=True)
            order_serializer = OrderSerializer(order, data=order_update_data, partial=True)
            product_serializer = ProductSerializer(product, data=product_update_data, partial=True)

            if (purchase_serializer.is_valid() and order_serializer.is_valid() and product_serializer.is_valid()):
                purchase_serializer.save()
                order_serializer.save()
                product_serializer.save()
                return Response({'purchase': purchase_serializer.data, 'order': order_serializer.data, 'product': product_serializer.data}, status=status.HTTP_200_OK)
            
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
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
            refund_result = performRefund(token, purchase.merchant_uid, purchase.price)
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