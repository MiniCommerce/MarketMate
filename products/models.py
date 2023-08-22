from django.db import models
from django.contrib.auth import get_user_model

import os
import uuid


# Create your models here.
User = get_user_model()

def image_path(instance, filename):
    filename = str(uuid.uui4())
    return os.path.join(f"product_image/{instance.title}", filename)


class Category(models.Model):
    name = models.CharField(blank=False, null=False, verbose_name='카테고리명')


class Product(models.Model):
    seller = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, verbose_name="판매자")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="카테고리")
    product_name = models.CharField(blank=False, null=False, max_length=200, verbose_name="상품명")
    price = models.IntegerField(blank=False, null=False, verbose_name="가격")
    amount = models.IntegerField(default=0, blank=False, null=False, verbose_name="수량")
    desc = models.TextField()
    score = models.FloatField(default=0, verbose_name="평점")
    thumbnail_image = models.ImageField(upload_to=image_path, blank=True, null=True, verbose_name="썸네일")
    status = models.CharField(max_length=30, verbose_name="상태")
    order_status = models.CharField(max_length=30, verbose_name="주문 상태")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False, on_delete=models.CASCADE, verbose_name="상품")
    image = models.ImageField(upload_to=image_path, verbose_name="상품 이미지")