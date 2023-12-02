from django.urls import path
from . import views

urlpatterns = [
    path('feeds/', views.feeds),
    path('comment_add/', views.comment_add),
    path('comment_del/<int:comment_id>/', views.comment_del)
]