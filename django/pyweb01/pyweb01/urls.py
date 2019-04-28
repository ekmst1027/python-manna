"""pyweb01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from bookmark import views

# 클라이언트에서 요청할 수 있는 url 정의
# url("url pattern", 실행할코드)
urlpatterns = [
    path('admin/', admin.site.urls),
    # r : 정규표현식, ^ : 시작, $ : 끝
    # http://localhost로 요청하면 views 모듈의 home 함수 실행
    url(r"^$", views.home),
    url(r"^detail$", views.detail)
]
