from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import PaymentResult
from .serializers import PaymentResultSerializer
from users.models import Buyer
from users.permissions import IsAuthenticated

from iamport import Iamport

class PaymentRequestView(APIView):
    def post(self, request):
        iamport = Iamport(
            code=settings.IAMPORT_CODE,
            api_key=settings.IAMPORT_API_KEY,
            api_secret=settings.IAMPORT_API_SECRET,
        )
        
        try:
            response = iamport.payment(
                merchant_uid="unique_merchant_uid",
                amount=100,
                name="Sample Product",
                buyer_email="buyer@example.com",
                buyer_name="Buyer Name",
                buyer_tel="010-1234-5678",
            )
            return Response({"redirect_url": response['redirect_url']}, status=status.HTTP_200_OK)
        except Iamport.ResponseErrorr as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)