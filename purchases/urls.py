from django.urls import path

from .views import OrderView, PrepurchaseView, PostpurchaseView, RefundView, BuyerOrdersView

app_name = "purchases"

urlpatterns = [
    path('order/', OrderView.as_view()),
    path('prepurchase/', PrepurchaseView.as_view()),
    path('postpurchase/', PostpurchaseView.as_view()),
    path('refund/', RefundView.as_view()),
    path('buyer_orders/', BuyerOrdersView.as_view()),
]