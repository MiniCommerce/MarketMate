from rest_framework import serializers

from .models import Product, ProductImage, Category


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
            ProductImage.objects.create(product=product, image=image)

        return product
    
    def update(self, instance, validated_data):
        change_name = validated_data.get('product_name', None)
        
        if change_name:
            instance.product_name = change_name
        
        if 'uploaded_images' in validated_data:
            uploaded_images = validated_data.pop('uploaded_images')
            # 이전 이미지 삭제
            instance.images.all().delete()
            # 새로 이미지 등록
            for image in uploaded_images:
                ProductImage.objects.create(product=instance, image=image)

        return super().update(instance, validated_data)







