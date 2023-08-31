from rest_framework import serializers

from .models import Product, ProductImage, Category
from utils.images import s3

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(child=serializers.ImageField(), max_length=10, write_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'    

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        product = Product.objects.create(**validated_data)
        
        for image in uploaded_images:
            image_path = s3.upload(image)
            ProductImage.objects.create(product=product, image=image_path)

        return product
    
    def update(self, instance, validated_data):
        if 'uploaded_images' in validated_data:
            uploaded_images = validated_data.pop('uploaded_images')
            
            # 이전 이미지 삭제    
            instance.images.all().delete()
            # 새로 이미지 등록
            for image in uploaded_images:
                image_path = s3.upload(image)
                ProductImage.objects.create(product=instance, image=image_path)

        return super().update(instance, validated_data)







