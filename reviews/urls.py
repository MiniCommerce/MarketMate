from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("list/", views.ReviewList.as_view()),
    path("write/", views.ReviewList.as_view()),
    path("update/", views.ReviewDetail.as_view()),
    path("delete/", views.ReviewDetail.as_view()),
]