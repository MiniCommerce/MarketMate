from django.urls import path
from . import views


app_name = "carts"

urlpatterns = [
    path("add/", views.CartView.as_view()),
    path("list/", views.CartView.as_view()),
    path("update/", views.CartView.as_view()),
]
