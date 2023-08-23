from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer
from users.permissions import IsAuthenticated

class ProductList(APIView):
    # 상품 전체 리스트 조회
    def get(self, request):
        products = Product.objects.all()

        if products:
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': '등록된 상품이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    

# 상품 등록
class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        seller =  request.user.seller

        if seller:
            category_name = request.data.pop('category')
            category, created = Category.objects.get_or_create(name=category_name)
            request_data = request.data.copy()
            request_data['seller'] = seller.pk
            request_data['category'] = category.pk
            serializer = ProductSerializer(data=request_data)

            if serializer.is_valid():        
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class ProductDetail(APIView):
    # 상품 상세 정보
    def get(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        serializer = ProductSerializer(product)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    # 상품 수정
    def patch(self, request):
        seller = request.user.seller
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        if seller.pk != product.seller_id:
            return Response({'message': '상품 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)