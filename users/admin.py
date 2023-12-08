from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class FollowersInline(admin.TabularInline):
    # user의 following의 중개 테이블 이용
    model = User.following.through
    # 내가 팔로우 할 때
    fk_name = 'from_user'
    verbose_name = '내가 팔로우 하고 있는 사용자'
    verbose_name_plural = f'{verbose_name} 목록'
    extra = 1


class FollowingInline(admin.TabularInline):
    model = User.following.through
    # 내가 팔로우 당할 때
    fk_name = 'to_user'
    verbose_name = '나를 팔로우하고 있는 사용자'
    verbose_name_plural = f'{verbose_name} 목록'
    extra = 1



# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (None, { 'fields': ('username', 'password')}),
        ('개인 정보', {'fields': ('first_name', 'last_name', 'email')}),
        ('추가 필드', {'fields': ('profile_image', 'short_description')}),
        ('권한', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('중요한 일정', {'fields':('last_login', 'date_joined')}),
        ('연관 객체', {'fields': ('like_posts',)})
    ]
    inlines = [
        FollowersInline,
        FollowingInline
    ]