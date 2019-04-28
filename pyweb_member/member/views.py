from django.shortcuts import render, redirect, render_to_response
# 회원가입폼과 로그인폼을 불러옴
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout
)

# 시작 페이지(http://localhost)
def home(request):
    # 로그인하지 않은 상태
    if not request.user.is_authenticated:
        data = {"username": request.user,
                "is_authenticated": request.user.is_authenticated}

    # 로그인 한 상태
    else:
        data = {"last_login": request.user.last_login,
                "username": request.user.username,
                "password": request.user.password,
                "is_authenticated": request.user.is_authenticated}

    # index.html로 포워딩되어 화면에 출력됨
    # return render_to_response("index.html")
    return render(request, "index.html")    # 위와 같은 코드

# 회원 가입 페이지(http://localhost/join)
@csrf_exempt
def join(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        # 입력값에 문제가 없으면(모든 유효성 검증 규칙을 통과할 때)
        if form.is_valid():
            # form.cleaned_data : 검증에 성공한 값들을 딕셔너리 타입으로 저장하고 있는 데이터
            # ** keyword argumentm 키워드 인자
            # 새로운 사용자가 생성됨
            new_user =\
                User.objects.create_user(**form.cleaned_data)
            # 로그인 처리
            django_login(request, new_user)
            # 시작 페이지로 이동
            return redirect("/")
        else: # 중복아이디, 비밀번호 규칙을 통과하지 못했을 때
            return render_to_response("index.html", 
                {"msg": "회원가입 실패... 다시 시도해보세요."})
    
    else: # get 방식
        # post 방식이 아닌 경우 회원가입페이지로 이동
        form = UserForm()
        return render(request, "join.html", {"form": form})
    
    return render(request, "index.html")

# 로그아웃 처리(http://localhost/logout)
def logout(request):
    # django에 내장된 로그아웃 처리 함수
    django_logout(request)
    # 시작페이지로 이동
    return redirect("/")

# 로그인 처리(http://localhost/login)
def login_check(request):
    # post방식일 때
    if request.method == "POST":
        # 사용자가 로그인 폼에 입력한 값
        form = LoginForm(request.POST) 
        name = request.POST["username"]
        pwd = request.POST["password"]
        # 인증
        user = authenticate(username=name, password=pwd)
        if user is not None: # 로그인 성공
            django_login(request, user)
            return redirect("/")
        else: # 로그인 실패
            return render_to_response("index.html",
                    {"msg": "로그인 실패... 다시 시도해 보세요."})
    else : # get 방식인 경우 - 로그인 페이지로 이동
        form = LoginForm()
        return render(request, "login.html", {"form": form})
