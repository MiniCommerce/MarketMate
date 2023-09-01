from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from users.models import Seller
from .models import Product, Category
from .serializers import ProductSerializer
from users.permissions import IsAuthenticated, IsSeller
from utils.images import s3

# 상품 조회
class ProductList(APIView):
    def get(self, request):
        category_name = request.GET.get('category')
        search_text = request.GET.get('search_text')
        products = None

        # 카테고리 검색
        if category_name:
            category = get_object_or_404(Category, name=category_name)
            products = Product.objects.filter(category=category.pk)
        # 텍스트를 통한 검색
        elif search_text:
            products = Product.objects.filter(product_name__icontains=search_text)
        # 전체 리스트
        else:
            products = Product.objects.exclude(product_status='StopSelling')

        if products:
            serialized_products = []
            
            for product in products:
                review_scores = product.review_set.values_list('score', flat=True)
                avg_score = round(sum(review_scores) / len(review_scores),1) if review_scores else 0
                
                product_data = ProductSerializer(product).data
                product_data['seller'] = product.seller.store_name
                product_data['score'] = avg_score
                serialized_products.append(product_data)

            return Response(serialized_products, status=status.HTTP_200_OK)
        
        return Response({'message': '등록된 상품이 없습니다.'}, status=status.HTTP_404_NOT_FOUND)


# 상품 등록
class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]
    
    def post(self, request):
        seller =  request.user.seller
        # 카테고리
        category_name = request.data.get('category')
        request.data.pop('category')
        category, created = Category.objects.get_or_create(name=category_name)
        # 썸네일 이미지
        thumbnail_image = request.data.get('thumbnail_image')
        request.data.pop('thumbnail_image')
        thumbnail_image_path = s3.upload(thumbnail_image)
        request_data = request.data.copy()
        request_data['seller'] = seller.pk
        request_data['category'] = category.pk
        request_data['thumbnail_image'] = thumbnail_image_path
        serializer = ProductSerializer(data=request_data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


class ProductDetail(APIView):
    # 상품 상세 정보
    def get(self, request):
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk=product_id)

        # 해당 상품에 연결된 리뷰의 점수들을 가져와서 평균 계산
        review_scores = product.review_set.values_list('score', flat=True)
        avg_score = round(sum(review_scores) / len(review_scores),1) if review_scores else 0

        serializer = ProductSerializer(product)
        serializer_data = serializer.data.copy()
        serializer_data['seller'] = product.seller.store_name
        serializer_data['score'] = avg_score

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
        
        thumbnail_image = request.data.get('thumbnail_image')

        if thumbnail_image:
            request.data.pop('thumbnail_image')
            thumbnail_image_path = s3.upload(thumbnail_image)
            request.data['thumbnail_image'] = thumbnail_image_path
                
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