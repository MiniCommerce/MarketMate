from rest_framework import serializers

from .models import PaymentResult

class PaymentResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentResult
        fields = '__all__'
