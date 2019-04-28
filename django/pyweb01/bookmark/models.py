from django.db import models

# Create your models here.
# 모델 클래스 정의 - django의 Model 클래스 상속
class Bookmark(models.Model):
    # 필드 선언
    # blank 빈값 허용 여부, null null 허용 여부
    title = models.CharField(max_length=100, blank=True, null=True)
    
    # unique : primary key
    url = models.URLField("url", unique=True)

    # 객체를 문자열로 표현하는 함수
    def __str__(self):
        return self.title