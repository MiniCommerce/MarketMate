from django.conf import settings
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import PaymentResult,Buyer
from iamport import Iamport



class PaymentInfoView(APIView):
    def post(self, request):
        iamport = Iamport(
            imp_key=settings.IAMPORT_KEY,
            imp_secret=settings.IAMPORT_SECRET
        )
        
        merchant_uid = request.data.get("merchant_uid")
        if not merchant_uid:
            return Response({"error": "merchant_uid is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = request.user
            if not user.is_authenticated:
                return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
            
            # 이메일 값을 사용하여 Buyer 객체 조회
            buyer = Buyer.objects.get(email=user.email)
            print(buyer)
            response = iamport.find(merchant_uid=merchant_uid)
            print(response)
            imp_uid = response.get("imp_uid")
            merchant_uid = response.get("merchant_uid")
            amount = response.get("amount")
            payment_status = response.get("status")  
            
            # 추출한 정보를 DB에 저장
            PaymentResult.objects.create(
                buyer=buyer,
                imp_uid=imp_uid,
                merchant_uid=merchant_uid,
                amount=amount,
                status=payment_status,  
            )
            return Response({"message": "Payment data saved successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)