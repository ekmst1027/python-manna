from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url, include
from board import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 게시물 목록(http://localhost)
    path('', views.list),
    # 글쓰기 페이지(http://localhost/write)
    path('write', views.write),
    # 글 저장(http://localhost/insert)
    path('insert', views.insert),
    # 파일 다운로드(http://localhost/download)
    path('download', views.download)
]

# 디버그 툴바 관련 url mapping
if settings.DEBUG:
    import debug_toolbar
    # debug_toolbar의 url 패턴 정의
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]