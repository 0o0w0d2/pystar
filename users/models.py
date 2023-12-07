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
    following = models.ManyToManyField(
        # 같은 테이블 user-user끼리의 관계
        'self',
        verbose_name='팔로우 중인 사용자들',
        related_name='followers',
        # 비대칭 관계
        symmetrical=False,
        # 중개 테이블
        through='users.Relationship'
    )

    def __str__(self):
        return self.username


# 다대다 연결 중개 테이블 직접 생성하기 (관계)
class Relationship(models.Model):
    # 누가
    from_user = models.ForeignKey(
        'users.User',
        verbose_name='팔로우를 요청한 사용자',
        related_name='following_relationships',
        on_delete=models.CASCADE
    )

    # 누구를
    to_user = models.ForeignKey(
        'users.User',
        verbose_name='팔로우 요청의 대상',
        related_name='follower_relationships',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'관계 {self.from_user} -> {self.to_user}'