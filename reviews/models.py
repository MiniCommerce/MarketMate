from django.db import models
from django.contrib.auth import get_user_model

from products.models import Product

# Create your models here.
User = get_user_model()


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="리뷰작성자")
    desc = models.CharField(max_length=200, verbose_name="상세설명")
    score = models.FloatField(min_value=0, max_value=5, verbose_name="평점")
    created_at = models.DateTimeField(auto_now_add=True)