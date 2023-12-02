from django.shortcuts import render, redirect
from .models import Post, PostImage, Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated :
        return redirect('/users/login/')

    comment_form = CommentForm()
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'comment_form': comment_form
    }

    return render(request, 'posts/feeds.html', context)

# 댓글 작성 처리를 위한 / POST 요청만 허용
@require_POST
def comment_add(request):
    print(request.POST)

    # commentForm 인스턴스 생성
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # comment 객체 생성
        comment = form.save(commit=False)

        # request에서 유저 정보 가져옴
        comment.user = request.user

        # DB에 저장
        comment.save()

        # comment에 연결된 post의 id값을 가져와 redirect
        return HttpResponseRedirect(f'/posts/feeds/#post-{comment.post.id}')