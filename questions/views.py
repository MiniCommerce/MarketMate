from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from purchases.models import Item, Order

from users.models import Buyer, Seller, User
from .models import Question
from .serializers import QuestionSerializer
from products.models import Product
from users.permissions import IsAuthenticated, IsBuyer


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


# 문의 리스트 
class QuestionList(APIView):
    def get(self, request):
        product_id = request.GET.get('product_id')
        product = get_object_or_404(Product, pk=product_id)
        questions = Question.objects.filter(product=product)
        serializer = QuestionSerializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

# 문의 작성
class CreateQuestion(APIView):
    permission_classes = [IsAuthenticated, IsBuyer]

    def post(self, request):
        product_id = request.data.pop('product_id')
        product = get_object_or_404(Product, pk=product_id)
        buyer = request.user.buyer
        
        if not(check_order(buyer, product)):
            return Response({
                'error_code': status.HTTP_401_UNAUTHORIZED,
                'error': '권한이 없습니다.'
                },
                status=status.HTTP_401_UNAUTHORIZED)
            
        request_data = request.data.copy()
        request_data['product'] = product.pk
        request_data['user'] = buyer.pk
        serializer = QuestionSerializer(data=request_data)
        
        if serializer.is_valid():                    
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({
            'error_code': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)


class QuestionDetail(APIView):
    permission_classes = [IsAuthenticated]

    # 문의, 답변 수정
    def patch(self, request):
        user_id = request.user.id
        question_id = request.data.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        
        buyer = Buyer.objects.filter(pk=user_id)

        if buyer:
            if user_id != question.user.id:
                return Response({
                    'error_code': status.HTTP_401_UNAUTHORIZED,
                    'error': '권한이 없습니다.'
                    },
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            if question.product.seller.id != user_id:
                return Response({
                    'error_code': status.HTTP_401_UNAUTHORIZED,
                    'error': '권한이 없습니다.'
                    },
                    status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = QuestionSerializer(question, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({
            'error_code': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST)


    # 문의, 답변 삭제
    def delete(self, request):
        user_id = request.user.id
        question_id = request.data.get('question_id')
        question = get_object_or_404(Question, pk=question_id)
        buyer = Buyer.objects.filter(pk=user_id)

        if buyer:
            if user_id != question.user.id:
                return Response({
                    'error_code': status.HTTP_401_UNAUTHORIZED,
                    'error': '권한이 없습니다.'
                    }, 
                    status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error_code': status.HTTP_401_UNAUTHORIZED,
                'error': '권한이 없습니다.'
                },
                status=status.HTTP_401_UNAUTHORIZED)
        
        question.delete()

        return Response({'message': '성공'}, status=status.HTTP_200_OK)