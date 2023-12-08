from django.shortcuts import render, redirect, get_object_or_404
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
    posts = Post.objects.all().order_by('-id')

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

            tag_string = request.POST.get('tags')
            if tag_string :
                tag_names = [tag.strip() for tag in tag_string.split(',')]
                for tag_name in tag_names:
                    # get_or_create로 생성하거나 가져온 HashTag 객체를 post에 tags에 추가
                    # {get이나 create된 객체}, {생성 여부} = Model.objects.get_or_create
                    tag, _ = HashTag.objects.get_or_create(name=tag_name)
                    post.tags.add(tag)

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

        # GET으로 'next' 값을 전달받았다면, 전달받은 'next'로 이동
        # url_next = request.GET.get('next') or reverse("posts:feeds") + f'#post-{comment.post.id}'
        # 앞의 값이 True면 앞이 할당, False면 뒤가 할당 => Boolean Operation
        if request.GET.get('next'):
            url_next = request.GET.get('next')
        else :
            url_next = reverse('posts:feeds') + f'#post-{comment.post.id}'

        return HttpResponseRedirect(url_next)


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
        posts = Post.objects.filter(tags=tag).order_by('-id')

    context = {
        'posts' : posts,
        'tag_name': tag_name
    }

    return render(request, 'posts/tags.html', context)


def post_detail(request, post_id):
    post = Post.objects.get(id = post_id)
    comment_form = CommentForm()

    context = {
        'post': post,
        'comment_form': comment_form
    }
    print(post)
    return render(request, 'posts/post_detail.html', context)


def post_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    # 유저가 좋아요한 Post 목록에 해당 Post가 존재한다면, 좋아요 목록에서 삭제
    if user.like_posts.filter(id=post.id).exists():
        user.like_posts.remove(post)

    # 좋아요한 Post 목록에 없다면, 좋아요 목록에 추가
    else :
        user.like_posts.add(post)

    url_next = request.GET.get('next') or reverse('posts:feeds') + f'#post-{post.id}'
    return HttpResponseRedirect(url_next)

def post_edit(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(instance=post)

    # 해쉬태그도 불러와야함, 사진도 불러와야 함(근데 사진을 불러올 수가 있나?)

    context = {
        'form': form
    }

    return render(request, 'posts/post_edit.html', context)

@require_POST
def post_del(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user == post.user:
        post.delete()
        return redirect('posts:feeds')

    else:
        return HttpResponseForbidden('글 삭제 권한이 없습니다.')

