from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from .models import User

# Create your views here.
def login_view(request):
    # 로그인 상태일 시 redirect
    if request.user.is_authenticated:
        return redirect('/posts/feeds/')

    if request.method == "POST":
        # POST된 data를 form에 넣은 객체 생성
        form = LoginForm(data=request.POST)

        # 유효성 검사
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # username, password에 해당하는 user 검사
            user = authenticate(username=username, password=password)

            # user가 존재할 때
            if user:
                # 로그인 상태로 변환 및 유지
                login(request, user)
                return redirect('/posts/feeds/')
            # user가 없을 때(return 값이 없음)
            else:
                form.add_error(None, '입력한 정보를 다시 확인해주세요.')

        # 유효성 검사 실패 or user가 없을 때
        context = {'form': form}
        return render(request, 'users/login.html', context)

    # request.method == GET
    else :
        form = LoginForm()
        context = {'form': form}
        return render(request, 'users/login.html', context)


def logout_view(request):

    logout(request)
    return redirect('/users/login/')


def signup(request):
    # POST 요청
    if request.method == "POST":
        form = SignupForm(data=request.POST, files=request.FILES)
        # 유효성 검사
        if form.is_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            profile_image = form.cleaned_data['profile_image']
            short_description = form.cleaned_data['short_description']

            User.objects.create_user(
                username=username,
                password=password1,
                profile_image=profile_image,
                short_description=short_description
            )

            return redirect('/users/login')

        # is_valid가 False(폼 유효성 검사 탈락)
        else :
            return render(request, 'users/signup.html', {'form': form})


    # GET 요청
    else :
        form = SignupForm()
        return render(request, 'users/signup.html', {'form': form})

