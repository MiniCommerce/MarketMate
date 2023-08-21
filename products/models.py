from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
User = get_user_model()

class Product(models.Model):
    CATEGORY = (
        ('의류 및 패션', '의류 및 패션'),
        ('전자제품', '전자제품'),
        ('가구 및 인테리어', '가구 및 인테리어'),
        ('뷰티 및 화장품', '뷰티 및 화장품'),
        ('스포츠 및 여가활동', '스포츠 및 여가활동'),
        ('식품 및 음료', '식품 및 음료'),
        ('유아 및 출산용품', '유아 및 출산용품'),
        ('도서 및 문구용품', '도서 및 문구용품'),
        ('자동차 및 오토바이', '자동차 및 오토바이'),
        ('기술 및 가전제품', '기술 및 가전제품')
    )

    seller = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, verbose_name='판매자')
    category = models.CharField(max_length=50, choices=CATEGORY, verbose_name='카테고리')
    name = models.CharField(blank=False, null=False, max_length=200, verbose_name='상품명')
    price = models.IntegerField(blank=False, null=False, verbose_name='가격')
    amount = models.IntegerField(default=0, blank=False, null=False, verbose_name='수량')
    desc = models.TextField()
    score = models.FloatField(default=0, verbose_name='평점')
    status = models.CharField(max_length=30, verbose_name='상태')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')