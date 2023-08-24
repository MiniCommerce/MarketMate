from django.urls import path

from .views import OrderView, PrepurchaseView, PostpurchaseView


urlpatterns = [
    path('order/', OrderView.as_view()),
    path('prepurchase/', PrepurchaseView.as_view()),
    path('postpurchase/', PostpurchaseView.as_view()),
]