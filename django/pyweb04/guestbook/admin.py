from django.contrib import admin
from guestbook.models import Guestbook

class GuestbookAdmin(admin.ModelAdmin):
    # 관리자 페이지에서 관리할 필드 목록을 튜플 형식으로 지정
    list_display = ("name", "email", "passwd", "content")

# 관리자 페이지에서 지원할 클래스를 등록
admin.site.register(Guestbook, GuestbookAdmin)