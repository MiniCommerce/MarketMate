from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Review
from purchases.models import Order, Item
from .serializers import ReviewSerializer
from products.models import Product
from users.permissions import IsAuthenticated, IsBuyer


# 상품 후기 리스트
class ReviewList(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            reviews = Review.objects.filter(product=product)
            serialized_reviews = []

            for review in reviews:
                serialized_review = ReviewSerializer(review).data
                serialized_review["buyer_name"] = review.buyer.nickname
                serialized_reviews.append(serialized_review)

            return Response(serialized_reviews, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response("Product not found.", status=status.HTTP_404_NOT_FOUND)
    
def check_order(buyer, product):
    orders = Order.objects.filter(buyer=buyer)

    if not(orders):
        return False

    for order in orders:
        items = Item.objects.filter(order_id=order.pk)
        for item in items:
            if item.product == product:
                return True

    return False

# 상품 후기 작성
class CreateReview(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        buyer = request.user.buyer

        if not(check_order(buyer, product)):
            return Response({'message':'상품 구매자만 후기를 작성할 수 있습니다.','status':401},status=status.HTTP_401_UNAUTHORIZED)

        if buyer and product:
            request_data = request.data.copy()
            request_data['buyer'] = buyer.pk
            request_data['product'] = product.pk
            serializer = ReviewSerializer(data=request_data)

            if serializer.is_valid():        
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    #  상품 후기 수정
    def patch(self, request):
        buyer = request.user.buyer

        try:
            review = Review.objects.get(pk=request.data.get('review_id'))
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if buyer.pk != review.buyer_id:
            return Response({'error': '리뷰 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        elif buyer.pk == review.buyer_id:
            serializer = ReviewSerializer(review, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        

    #  상품 후기 삭제
    def delete(self, request):
        buyer = request.user.buyer

        try:
            review = Review.objects.get(pk=request.data.get('review_id'))
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if buyer.pk != review.buyer_id:
            return Response({'error': '리뷰 삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)