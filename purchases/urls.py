from django.urls import path

from .views import OrderView, PurchaseView


urlpatterns = [
    path('order/', OrderView.as_view()),
    path('purchase/', PurchaseView.as_view()),
]