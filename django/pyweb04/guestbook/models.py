from django.db import models
from datetime import datetime

# 방명록 테이블
class Guestbook(models.Model):
    # 자동 증가 일련번호 필드(integer 자료형으로 저장됨)
    idx = models.AutoField(primary_key=True)
    # null값을 허용하지 않음
    name = models.CharField(null=False, max_length=50)
    email = models.CharField(null=False, max_length=50)
    passwd = models.CharField(null=False, max_length=50)
    # TextField 대용량 텍스트
    content = models.TextField(null=False, max_length=50)
    # 날짜가 입력되지 않으면 현재 시각을 저장
    post_date = models.DateTimeField(default=datetime.now, blank=True)
