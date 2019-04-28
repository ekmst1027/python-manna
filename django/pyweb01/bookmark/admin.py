from django.contrib import admin
from bookmark.models import Bookmark

# Register your models here.
# 관리자 사이트에서 Bookmark 클래스가 어떤 모습으로 출력될지 정의하는 코드
class BookmarkAdmin(admin.ModelAdmin):
    # 관리자 화면에 출력할 필드 목록(튜플 형식)
    list_display = ("title", "url")

# Bookmark 클래스와 BookmarkAdmin 클래스를 등록
admin.site.register(Bookmark, BookmarkAdmin)