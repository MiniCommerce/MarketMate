from django.db import models

from products.models import Product
from users.models import Buyer


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name="리뷰작성자")
    desc = models.CharField(max_length=200, verbose_name="리뷰내용")
    score = models.FloatField(verbose_name="평점")
    created_at = models.DateTimeField(auto_now_add=True)