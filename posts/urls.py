from django.urls import path
from . import views

urlpatterns = [
    path('feeds/', views.feeds),
    path('comment_add/', views.comment_add)
]