from rest_framework import serializers

from .models import Order, Purchase


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"


class PurchaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Purchase
        fields = "__all__"