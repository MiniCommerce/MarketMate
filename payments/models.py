from django.db import models

from users.models import Buyer 

class PaymentResult(models.Model):
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)  
    imp_uid = models.CharField(max_length=100)
    merchant_uid = models.CharField(max_length=100)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentResult for {self.buyer.nickname} - {self.merchant_uid}"