from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone

# Create your models here.

class UserManager(BaseUserManager):
    
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('User must have an email')
        now = timezone.now() 
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            last_login=now,
            date_joined=now,
            **extra_fields
        )
        user.set_password(password) 
        user.save(using=self._db) 
        return user
    
    # create_user
    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)
    
    # create_superuser
    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

number_regex = RegexValidator(
    regex=r'[0-9]{2,}[-]?[0-9]{4,}[-]?[0-9]{4,}',
    message="전화번호 형식은 {010-1234-1234, 01012341234}에 20자 이하로 이루어져야 합니다."
)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, max_length=255)
    name = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(validators=[number_regex], max_length=20, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()


class Buyer(User):
    nickname = models.CharField(max_length=20, null=False, blank=True)
    shipping_address = models.CharField(max_length=50, null=False, blank=True)
    
    def __str__(self):
        return self.nickname


class Seller(User):
    store_name = models.CharField(max_length=20, null=False, blank=True)
    shipping_place = models.CharField(max_length=50, null=False, blank=True)

    def __str__(self):
        return self.store_name