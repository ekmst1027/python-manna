from django.db import models

# 설문조사 문항
# 테이블 : app이름_클래스이름 => survey_servey
class Survey(models.Model):
    # 설문 인덱스
    survey_idx = models.AutoField(primary_key=True)
    # 문제
    question = models.TextField(null=False)
    # 답 1~4
    ans1 = models.TextField(null=True)
    ans2 = models.TextField(null=True)
    ans3 = models.TextField(null=True)
    ans4 = models.TextField(null=True)
    # 설문진행상태(y=진행중, n=종료)
    status = models.CharField(max_length=1, default="y")

# 설문응답
# survey_answer
class Answer(models.Model):
    # 응답아이디(자동증가필드)
    answer_idx = models.AutoField(primary_key=True)
    # 설문아이디(Survey의 idx 필드와 연결되는 Foreing key)
    survey_idx = models.IntegerField()
    # 응답번호
    num = models.IntegerField()

