from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):

    short_description = models.TextField("간단 소개", blank=True)
    profile_image = models.ImageField(
        "프로필 사진", upload_to="users/profile", blank=True)
    like_posts = models.ManyToManyField(
        "posts.Post",
        verbose_name='좋아요 누른 Post 목록',
        related_name='like_users',
        blank=True
    )

    def __str__(self):
        return self.username
