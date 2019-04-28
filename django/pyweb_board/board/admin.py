from django.contrib import admin
from board.models import Board

class BoardAdmin(admin.ModelAdmin):
    # 관리자 페이지에 표시할 필드 목록을 튜플 형식으로 선언
    list_display = ("writer", "title", "content")

# 관리자 사이트에 테이블 등록
admin.site.register(Board, BoardAdmin)
