from django.urls import path
from .views import PaymentInfoView

app_name = "payment"

urlpatterns = [
    path('list/', PaymentInfoView.as_view(), name='paymentlist'),
]