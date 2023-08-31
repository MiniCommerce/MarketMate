from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("list/<int:pk>/", views.ReviewList.as_view()),
    path("write/", views.CreateReview.as_view()),
    path("update/", views.ReviewDetail.as_view()),
    path("delete/", views.ReviewDetail.as_view()),
]