from django.urls import path
from . import views

app_name = "qeustions"

urlpatterns = [
    path("list/", views.QuestionList.as_view(), name="문의리스트"),
    path("write/", views.CreateQuestion.as_view(), name="문의작성"),
    # path("update/", views.QuestionDetail.as_view(), name="문의수정"),
    path("delete/", views.QuestionDetail.as_view(), name="문의삭제"),
]