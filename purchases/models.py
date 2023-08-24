from django.db import models

from users.models import Buyer, Seller
from products.models import Product


# Create your models here.
class Order(models.Model):
    product = models.ForeignKey(Product, blank=False, null=False, on_delete=models.CASCADE, verbose_name="상품")
    buyer = models.ForeignKey(Buyer, blank=False, null=False, on_delete=models.CASCADE, verbose_name="구매자")
    seller = models.ForeignKey(Seller, blank=False, null=False, on_delete=models.CASCADE, verbose_name="판매자")
    order_name = models.CharField(max_length=100, verbose_name="주문명")
    status = models.CharField(max_length=20, verbose_name="주문 진행 상태")
    address = models.CharField(max_length=50, verbose_name="배송지")
    price = models.IntegerField(verbose_name="가격")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="주문일")


class Purchase(models.Model):
    order = models.ForeignKey(Order, blank=False, null=False, on_delete=models.CASCADE, verbose_name="주문")
    buyer = models.ForeignKey(Buyer, blank=False, null=False, on_delete=models.CASCADE, verbose_name="구매자")
    imp_uid = models.CharField(max_length=320, blank=True, null=True, verbose_name="결제번호")
    merchant_uid = models.CharField(max_length=320, blank=False, null=False, verbose_name="주문번호")
    purchase_type = models.CharField(max_length=20, verbose_name="결제 수단")
    status = models.CharField(max_length=20, verbose_name="결제 진행 상태")
    price = models.IntegerField(verbose_name="가격")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="결제일")