from django.db import models

from products.models import Product
from users.models import Buyer


class Question(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="상품")
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, verbose_name="질문작성자")
    desc = models.CharField(max_length=200, verbose_name="질문")
    answer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="답변")
    created_at = models.DateTimeField(auto_now_add=True)