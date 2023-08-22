from django.db import models

from products.models import Product
from users.models import Buyer


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name="구매자")
    amount = models.IntegerField(default=0, verbose_name="수량")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일")