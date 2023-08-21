from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

from .models import Buyer, Seller

User = get_user_model()

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
    

# 임시 참고용
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': '비밀번호가 일치하지 않습니다.'})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data['email'],
            password = validated_data['password'],
        )
        # 토큰 생성
        Token.objects.create(user=user) 
        return user
    
    class LoginSerializer(serializers.Serializer):
        email = serializers.CharField(required=True)
        password = serializers.CharField(required=True, write_only=True)

        def validate(self, data):
            user = authenticate(**data)
            
            if user:
                token = Token.objects.get(user=user)
                return token
            raise serializers.ValidationError("유효하지 않은 로그인입니다.")