from django.contrib import admin
from .models import User, Buyer, Seller

admin.site.register(User)
admin.site.register(Buyer)
admin.site.register(Seller)