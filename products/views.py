from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import Seller
from .models import Product, Category
from .serializers import ProductSerializer
from users.permissions import IsAuthenticated, IsSeller


# 상품 조회
class ProductList(APIView):
    def get(self, request):
        category_id = request.data.get('category')
        search_text = request.data.get('search_text')
        products = None

        # 카테고리 검색
        if category_id:
            products = Product.objects.filter(category=category_id)
        # 텍스트를 통한 검색
        elif search_text:
            products = Product.objects.filter(product_name__icontains=search_text)
        # 전체 리스트
        else:
            products = Product.objects.exclude(product_status='StopSelling')

        if products:
            serializer = ProductSerializer(products, many=True)
            
            for i in range(len(serializer.data)):
                serializer.data[i]['seller'] = Product.objects.get(pk=serializer.data[i].get("id")).seller.store_name

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': '등록된 상품이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


# 상품 등록
class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]
    
    def post(self, request):
        seller =  request.user.seller

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
        product = get_object_or_404(Product, pk=request.GET.get('product_id'))
        serializer = ProductSerializer(product)

        serializer_data = serializer.data.copy()
        serializer_data['seller'] = Product.objects.get(pk=serializer.data.get("id")).seller.store_name

        return Response(serializer_data, status=status.HTTP_200_OK)
        
    # 상품 수정
    def patch(self, request):
        try:
            seller = request.user.seller
        except:
            return Response({'message': '상품 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
            
        product_id = request.data.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        if seller.pk != product.seller_id:
            return Response({'message': '상품 수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '상품이 성공적으로 수정되었습니다.', 'data': serializer.data, 'status':200}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# 내 등록 상품 조회
class Saleproduct(APIView):
    permission_classes = [IsAuthenticated, IsSeller]
    
    def get(self, request):
        seller = request.user.seller
        products = Product.objects.filter(seller=seller)
        
        if products:
            serializer = ProductSerializer(products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    
        return Response({'message': '등록된 상품이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)