from django import forms
from django.contrib.auth.models import User

# 회원가입폼
class UserForm(forms.ModelForm):
    # 메타클래스(클래스를 생성하는 클래스)
    class Meta:
        model = User # django에 내장된 회원정보폼
        # 회원가입폼에 사용할 필드 선언
        fields = ["username", "email", "password"]

# 로그인폼(아이디와 비밀번호만 입력받음)
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]