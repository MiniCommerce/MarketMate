from django.contrib import admin

from .models import Order, Purchase


# Register your models here.
admin.site.register(Order)
admin.site.register(Purchase)