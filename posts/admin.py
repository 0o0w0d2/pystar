# admin을 조작해서 썸네일 표시할 때 필요한 모듈
# from django.contrib.admin.widgets import AdminFileWidget
# from django.db import models
# from django.utils.safestring import mark_safe

import admin_thumbnails
from django.contrib import admin
from .models import Post, PostImage, Comment, HashTag
from django.db.models import ManyToManyField
from django.forms import CheckboxSelectMultiple

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1

# admin을 조작해서 썸네일 표시
# class InlineImageWidget(AdminFileWidget):
#     def render(self, name, value, attrs=None, renderer=None):
#         html = super().render(name, value, attrs, renderer)
#         if value and getattr(value, 'url', None):
#             html = mark_safe(f'<img src="{value.url}" height="150">' + html)
#         return html

@admin_thumbnails.thumbnail('photo')
class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 1
    # admin을 조작해서 썸네일 표시할 때 추가해야할 코드
    # formfield_overrides = {
    #     models.ImageField: {
    #         'widget': InlineImageWidget
    #     }
    # }

class LikeUserInline(admin.TabularInline):
    model = Post.like_users.through
    verbose_name = '좋아요 한 User'
    verbose_name_plural = f'{verbose_name} 목록'
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False





# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'content'
    ]
    inlines = [
        CommentInline,
        PostImageInline,
        LikeUserInline
    ]
    formfield_overrides = {
        ManyToManyField: { 'widget': CheckboxSelectMultiple }
    }


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'post', 'photo'
    ]


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = [
        'id', 'post', 'content'
    ]


@admin.register(HashTag)
class HashTagAdmin(admin.ModelAdmin):
    pass

