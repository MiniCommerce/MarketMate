from django.urls import path
from . import views

app_name = "qeustions"

urlpatterns = [
    path("list/", views.QuestionList.as_view()),
    path("write/", views.CreateQuestion.as_view()),
    path("update/", views.QuestionDetail.as_view()),
    path("delete/", views.QuestionDetail.as_view()),
]