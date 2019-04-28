from django.db import models
from datetime import datetime

# 게시판 테이블
class Board(models.Model):
    # 게시물 번호, 자동증가 필드
    idx = models.AutoField(primary_key=True)
    writer = models.CharField(null=False, max_length=50)
    title = models.CharField(null=False, max_length=120)

    # 조회수, 기본값 0
    hit = models.IntegerField(default=0)
    content = models.TextField(null=False)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
    filename = models.CharField(\
        null=True, blank=True, default="", max_length=500)
    filesize = models.IntegerField(default=0)
    down = models.IntegerField(default=0)

    # 조회수 증가 처리 함수
    def hit_up(self):
        self.hit += 1

    # 다운로드 횟수 증가 처리 함수
    def down_up(self):
        self.down += 1

# 댓글 테이블
class Comment(models.Model):
    idx = models.AutoField(primary_key=True)
    board_idx = models.IntegerField(null=False)
    writer = models.CharField(null=False, max_length=50)
    content = models.TextField(null=False)
    post_date = models.DateTimeField(default=datetime.now, blank=True)
