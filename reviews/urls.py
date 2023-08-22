from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("list/<int:product_id>/", views.ReviewList.as_view()),
    path("write/<int:product_id>/", views.ReviewList.as_view()),
    path("update/<int:review_id>/", views.ReviewDetail.as_view()),
    path("delete/<int:review_id>/", views.ReviewDetail.as_view()),
]