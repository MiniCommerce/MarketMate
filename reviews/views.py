from django.shortcuts import render
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Review
from .serializers import ReviewSerializer


class ReviewList(APIView):
    # 상품 후기 리스트
    def get(self, request, product_id):
        reviews = Review.objects.filter(product=product_id)
        serializer = ReviewSerializer(reviews, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 상품 후기 작성
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        serializer = ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(APIView):
    permission_classes = [IsAuthenticated]

    #  상품 후기 수정
    def patch(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if review.user != request.user:
            return Response({'error': '이 리뷰를 수정할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ReviewSerializer(review, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  상품 후기 삭제
    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
        except Review.DoesNotExist:

            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if review.user != request.user:
            return Response({'error': '이 리뷰를 삭제할 수 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)