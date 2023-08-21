from django.urls import path

from .views import ProductView, ProductListView


urlpatterns = [
    path('create/', ProductView.as_view()),
    path('detail/', ProductView.as_view()),
    path('detail/update/', ProductView.as_view()),
    path('detail/delete/', ProductView.as_view()),
    path('list/', ProductListView.as_view()),
]