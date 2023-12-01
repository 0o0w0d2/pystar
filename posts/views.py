from django.shortcuts import render, redirect
from .models import Post, PostImage, Comment

# Create your views here.
def feeds(request):
    if not request.user.is_authenticated :
        return redirect('/users/login/')

    posts = Post.objects.all()

    return render(request, 'posts/feeds.html', {'posts' : posts})