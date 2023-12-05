from django.urls import path
from . import views


app_name= 'posts'

urlpatterns = [
    path('feeds/', views.feeds, name='feeds'),
    path('comment_add/', views.comment_add, name='comment_add'),
    path('comment_del/<int:comment_id>/', views.comment_del, name='comment_del'),
    path('post_add/', views.post_add, name='post_add'),
    path('tags/<str:tag_name>/', views.tags, name='tags'),
    path('<int:post_id>/', views.post_detail, name='post_detail')
]