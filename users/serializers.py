from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

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
    

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        
        if user:
            # 토큰 생성
            token, created = Token.objects.get_or_create(user=user)
            return token
        raise serializers.ValidationError("유효하지 않은 로그인입니다.")