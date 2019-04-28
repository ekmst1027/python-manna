from django import forms
from django.contrib.auth.models import User

# html로 폼을 직접 작성하지 않고 django의 내장 클래스로부터 폼을 자동 생성

# 회원가입 폼
class UserForm(forms.ModelForm):
    class Meta:
        # User 사용자 정보를 저장하는 클래스
        model = User
        # 회원가입폼에 표시될 필드(아이디, 이메일, 비번)
        fields = ["username", "email", "password"]

# 로그인 폼
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]