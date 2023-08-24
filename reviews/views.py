from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.models import Buyer
from .models import Review
from .serializers import ReviewSerializer
from products.models import Product
from users.permissions import IsAuthenticated


class ReviewList(APIView):
    # 상품 후기 리스트
    def get(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        reviews = Review.objects.filter(product=product)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 상품 후기 작성
    def post(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        buyer = get_object_or_404(Buyer, pk=Token.objects.get(key=request.auth).user_id)

        if buyer and product:
            request_data = request.data.copy()
            request_data['user'] = buyer.pk
            request_data['product'] = product.pk
            serializer = ReviewSerializer(data=request_data)

            if serializer.is_valid():        
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated]

    #  상품 후기 수정
    def patch(self, request):
        user = get_object_or_404(Buyer, pk=Token.objects.get(key=request.auth).user_id)

        try:
            review = Review.objects.get(pk=request.data.get('review_id'))
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if user.pk != review.user_id:
            return Response({'error': '이 리뷰를 수정할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        elif user.pk == review.user_id:
            serializer = ReviewSerializer(review, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        

    #  상품 후기 삭제
    def delete(self, request):
        user = get_object_or_404(Buyer, pk=Token.objects.get(key=request.auth).user_id)

        try:
            review = Review.objects.get(pk=request.data.get('review_id'))
        except Review.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if user.pk != review.user_id:
            return Response({'error': '이 리뷰를 삭제할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)