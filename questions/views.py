from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from users.models import Buyer, Seller, User
from .models import Question
from .serializers import QuestionSerializer
from products.models import Product

# Create your views here.

# 문의 리스트 
class QuestionList(APIView):
    def get(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        questions = Question.objects.filter(product=product, parent=None)
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 문의 작성
class CreateQuestion(APIView):
    def post(self, request):
        product = Product.objects.get(pk=request.data.get('product_id'))
        buyer = Buyer.objects.filter(pk=Token.objects.get(key=request.auth).user_id).first()
        seller = Seller.objects.filter(pk=Token.objects.get(key=request.auth).user_id).first()

        if product and (buyer or seller):
            request_data = request.data.copy()

            # 구매자 문의
            if "parent" not in request_data:
                request_data['user'] = buyer.pk
            # 판매자 답변
            elif "parent" in request_data:
                if product.seller_id == seller.pk:
                    request_data['user'] = seller.pk 
                else:
                    return Response({'error': '상품 판매자만 답변할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)
                
            request_data['product'] = product.pk
            serializer = QuestionSerializer(data=request_data)

            if serializer.is_valid():                    
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    # 문의, 답변 수정
    def patch(self, request):
        user = get_object_or_404(User, pk=Token.objects.get(key=request.auth).user_id)

        try:
            question = Question.objects.get(pk=request.data.get('question_id'))
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if user.pk != question.user_id:
            return Response({'error': '수정 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        
        elif user.pk == question.user_id:
            serializer = QuestionSerializer(question, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(status=status.HTTP_401_UNAUTHORIZED)


    # 문의, 답변 삭제
    def delete(self, request):
        user = get_object_or_404(User, pk=Token.objects.get(key=request.auth).user_id)

        try:
            question = Question.objects.get(pk=request.data.get('question_id'))
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if user.pk != question.user_id:
            return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

        question.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)