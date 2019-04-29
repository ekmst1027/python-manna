from django.db import models

# 상품 클래스
class Product(models.Model):
    # 상품코드, 숫자 일련번호
    product_id = models.AutoField(primary_key=True)
    # 상품이름
    product_name = models.CharField(null=False, max_length=150)
    # 가격
    price = models.IntegerField(default=0)
    # 상품설명
    description = models.TextField(null=False, max_length=500)
    # 상품이미지 경로
    picture_url = models.CharField(null=True, max_length=150)

# 장바쿠니 클래스
class Cart(models.Model):
    # 장바쿠니 코드, 숫자 일련번호
    cart_id = models.AutoField(primary_key=True)
    # 사용자이이디
    userid = models.CharField(null=False, max_length=150)
    # 상품코드
    product_id = models.IntegerField(default=0)
    # 수량
    amount = models.IntegerField(default=0)