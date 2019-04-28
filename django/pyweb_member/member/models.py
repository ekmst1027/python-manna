from django.db import models
from django import forms
from django.contrib.auth.models import User

# django의 내장 폼인 ModelForm을 상속받은 클래스
class UserForm(forms.ModelForm):
    class Meta:
        # User 사용자 정보를 저장하는 기본 클래스
        model = User
        # 회원가입폼, 로그인폼에서 사용할 필드 정의
        fields = ["username", "email", "password"]

