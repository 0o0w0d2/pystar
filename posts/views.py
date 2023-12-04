from django.shortcuts import render, redirect
from .models import Post, PostImage, Comment, HashTag
from .forms import CommentForm, PostForm
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated :
        return redirect('users:login')

    comment_form = CommentForm()
    posts = Post.objects.all()

    context = {
        'posts': posts,
        'comment_form': comment_form
    }

    return render(request, 'posts/feeds.html', context)

def post_add(request):


    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            for image in request.FILES.getlist('images') :
                PostImage.objects.create(
                    post=post,
                    photo=image
                )
            url = reverse('posts:feeds') + f'#post-{post.id}'
            return HttpResponseRedirect(url)

    else :
        form = PostForm()

    context = {'form': form}
    return render(request, 'posts/post_add.html', context)


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
        url = reverse('posts:feeds') + f'#post-{comment.post.id}'
        return HttpResponseRedirect(url)


@require_POST
def comment_del(request, comment_id):
    if request.method == 'POST':
        comment = Comment.objects.filter(id=comment_id)[0]

        if comment.user == request.user :
            comment.delete()
            url = reverse('posts:feeds') + f'#post-{comment.post.id}'
            return HttpResponseRedirect(url)
        else :
            # 요청 데이터는 유효하나 해당 요청을 실행할 권한이 없다(status code:403)
            return HttpResponseForbidden('댓글 삭제 권한이 없습니다.')



def tags(request, tag_name):
    # Post와 Tag가 서로 객체 형태로 연결되어있으니, Tag의 name이 tag_name과 같은 Tag 객체를 가져오고,
    # 가져온 Tag를 토대로 Post에서 filter
    try:
        tag = HashTag.objects.get(name=tag_name)
    # DoesNotExist error 발생 시, 빈 QuerySet 반환
    except HashTag.DoesNotExist:
        posts = Post.objects.none()
    else :
        posts = Post.objects.filter(tags=tag)

    context = {
        'posts' : posts,
        'tag_name': tag_name
    }

    return render(request, 'posts/tags.html', context)