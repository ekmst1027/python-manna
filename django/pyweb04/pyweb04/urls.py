from django.contrib import admin
from django.urls import path
from guestbook import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 방명록 리스트(http://localhost)
    path('', views.list),
    # 글쓰기 페이지로 이동(http://localhost/write)
    path('write', views.write), 
    # 글저장(http://localhost/gb_insert)
    path('gb_insert', views.insert),
    # 비밀번호 체크(http://localhost/passwd_check)
    path('passwd_check', views.passwd_check),
    # 방명록 수정(http://localhost/gb_update)
    path('gb_update', views.update),
    # 방명록 삭제(http://localhost/gb_delete)
    path('gb_delete', views.delete),
]
