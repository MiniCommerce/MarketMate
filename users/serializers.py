from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Buyer, Seller


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['email', 'password', 'nickname', 'shipping_address', 'number']  
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Buyer.objects.create_user(**validated_data)
        return user


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['email', 'password', 'store_name', 'shipping_place', 'number'] 
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = Seller.objects.create_user(**validated_data)
        return user