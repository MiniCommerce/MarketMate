from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Cart(models.Model):
    product     =   models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    user       =   models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="구매자")
    amount      =   models.IntegerField(default=0, verbose_name="수량")
    created_at  =   models.DateTimeField(auto_now_add=True, verbose_name="생성일")