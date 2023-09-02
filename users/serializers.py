from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token

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
        
        if user and user.is_active:
            # 토큰 생성
            token, created = Token.objects.get_or_create(user=user)
            member = 'buyer' if hasattr(user, 'buyer') else 'seller'
            data = {
                'token': token,
                'user_id': user.pk,
                'member': member
            }
            return data
        
        raise serializers.ValidationError("유효하지 않은 로그인입니다.")


class BuyerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = ['nickname', 'number', 'shipping_address']  


class SellerUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ['store_name', 'number', 'shipping_place']  


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value


class DeleteUserSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, write_only=True)