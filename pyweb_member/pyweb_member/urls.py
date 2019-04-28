from django.contrib import admin
from django.urls import path
from member import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 시작 페이지(http://localhost)
    path('', views.home, name="/"),
    # 회원가입 페이지(http://localhost/join)
    path('join/', views.join),
    # 로그아웃 처리(http://localhost/logout)
    path('logout/', views.logout),
    # 로그인 처리(http://localhost/login)
    path('login/', views.login_check, name="login"),

]
