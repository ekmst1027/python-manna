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
    path('download', views.download),
    # 상세화면(http://localhost/detail)
    path('detail', views.detail), 
    path('detail/', views.detail),
    # 댓글 저장(http://localhost/reply_insert)
    path('reply_insert', views.reply_insert),
    # 게시물 수정(http://localhost/update)
    path('update', views.update),
    # 게시물 삭제(http://localhost/delete)
    path('delete', views.delete),
]

# 디버그 툴바 관련 url mapping
if settings.DEBUG:
    import debug_toolbar
    # debug_toolbar의 url 패턴 정의
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]