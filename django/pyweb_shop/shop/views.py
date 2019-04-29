import math
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.http import urlquote
from django.shortcuts import render, render_to_response, redirect
from .forms import UserForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    login as django_login,
    logout as django_logout,
)
from shop.models import Product, Cart

# 시작 페이지(http://localhost)
def home(request):
    if not request.user.is_authenticated:   # 로그인하지 않은 상태
        data = {"username": request.user,
                "is_authenticated": request.user.is_authenticated}
    else:   # 로그인 한 상태
        data = {"last_login": request.user.last_login,
                "username": request.user.username,
                "password": request.user.password,
                "is_authenticated": request.user.is_authenticated}
    return render(request, "index.html", context={"data": data})

# 상품목록(http://localhost/product_list)
def product_list(request):
    # 상품갯수
    count = Product.objects.count()
    # 상품리스트
    productList = Product.objects.order_by("product_name")
    # 상품목록 페이지로 넘어가서 출력됨
    return render_to_response(\
        "product_list.html", {"productList": productList, "count": count})

# 상품상세화면(http://localhost/product_detail)
def product_detail(request):
    # 상품코드
    pid = request.GET["product_id"]
    # 상품코드에 해당하는 레코드 선택 
    vo = Product.objects.get(product_id=pid)
    # product_detail.html 페이지로 이동
    # range(1, 21) => 1~20
    return render_to_response(\
        "product_detail.html", {"vo": vo, "range": range(1,21)})

# 장바구니에 상품 추가(http://localhost/cart_insert)
@csrf_exempt
def cart_insert(request):
    # 세션변수 userid 확인, 없으면 빈문자열이 리턴됨
    uid = request.session.get("userid", "")
    if uid != "": # 로그인한 상태
        vo = Cart(userid = uid,
                    product_id = request.POST["product_id"],
                    amount = request.POST["amount"])

        vo.save() # 장바구니 테이블에 추가
        return redirect("/cart_list")   # 장바구니 목록으로 이동

    else: # 로그인하지 않은 상태
        return redirect("/login")   # 로그인 페이지로 이동

# 로그인 처리(http://localhost/login)
def login_check(request):
    if request.method == "POST": # post 방식의 경우
        form = LoginForm(request.POST)  # 사용자가 입력한 로그인폼
        name = request.POST["username"] # 아이디
        pwd = request.POST["password"]  # 비번
        # 인증 처리
        user = authenticate(username=name, password=pwd)
        if user is not None:    # 결과값이 존재하면
            django_login(request, user) # 로그인 처리
            request.session["userid"] = name    # 세션변수 저장
            return redirect("/")    # 시작 페이지로 이동
        else:
            return render_to_response("index.html",
            {"msg": "로그인 실패... 다시 시도해 보세요."})

    else:   # get 방식의 경우
        form = LoginForm()  # 로그인 폼 저장
        return render(request, "login.html", {"form": form})

# 회원가입 페이지(http://localhost/join)
def join(request):
    if request.method == "POST":    # 회원가입폼을 채우고 전송한 경우
        form = UserForm(request.POST)   # 사용자가 입력한 회원가입폼
        if form.is_valid(): # 유효성 검증을 통과했으면
            # 새로운 계정이 테이블에 추가됨
            new_user = User.objects.create_user(**form.cleaned_data)
            django_login(request, new_user) # 로그인 처리
            return redirect("/")    # 시작 페이지로 이동
        else:
            return render_to_response("index.html",
            {"msg": "회원가입 실패... 다시 시도해 보세요."})

    else:   # 회원가입폼으로 이동
        form = UserForm()   # 회원가입폼 생성
        return render(request, "join.html", {"form": form})

    return render(request, "index.html")

# 로그아웃 처리(http://localhost/logout)
def logout(request):
    # django에 내장된 로그아웃 처리 함수 호출
    django_logout(request)

    # 모든 세션변수를 순회하면서 삭제 처리
    for sesskey in request.session.keys():
        del request.session[sesskey]

    # 시작 페이지로 이동
    return redirect("/")

# 장바구니 목록(http://localhost/cart_list)
def cart_list(request):
    # 세션 체크
    uid = request.session.get("userid", "")
    # 세션이 존재하면(로그인한 상태)
    if uid != "":
        # 레코드 갯수
        cartCount = Cart.objects.count()
        # 복잡한 sql의 경우 모델클래스.object.raw(sql문장)
        cartList = Cart.objects.raw("""
        SELECT cart_id, userid, amount, c.product_id, product_name, price, amount*price money
        FROM shop_cart c, shop_product p
        WHERE c.product_id = p.product_id and userid='{0}'
        """.format(uid))

        sumMoney = 0    # 금액 합계
        fee = 0 # 배송료
        sum = 0 # 배송료를 포함한 합계

        if cartCount > 0:
            # 장바구니 금액 합계(raw 쿼리에는 반드시 primary key가 포함되어야 함)
            # 금액 합계
            sumRow = Cart.objects.raw("""
            SELECT sum(amount*price) cart_id
            FROM shop_cart c, shop_product p
            WHERE c.product_id = p.product_id and userid='{0}'
            """.format(uid))

            sumMoney = sumRow[0].cart_id
            
            # 배송료(5만원 이상이면 면제, 5만원 미만이면 2500원)
            if sumMoney != None and sumMoney > 50000:
                fee = 0
            else:
                fee = 2500

            if sumMoney != None:
                sum = sumMoney + fee
            else:
                sumMoney = 0
                sum = 0

        return render_to_response(\
            "cart_list.html", {"cartList": cartList,
                                "cartCount": cartCount,
                                "sumMoney": sumMoney,
                                "fee": fee,
                                "sum": sum})

    else: # 로그인하지 않은 상태
        return redirect("/login")

# 장바구니 업데이트(http://localhost/cart_update)
@csrf_exempt
def cart_update(request):
    uid = request.session.get("userid", "") # 세션변수
    if uid != "":   # 세션값이 있으면(로그인한 상태)
        # 폼 데이터가 배열값인 경우 getlist("배열이름")
        amt = request.POST.getlist("amount")
        cid = request.POST.getlist("cart_id")
        pid = request.POST.getlist("product_id")
        for idx in range(len(cid)):
            vo = Cart(cart_id = cid[idx],
                        userid = uid,
                        product_id = pid[idx],
                        amount = amt[idx])
        vo.save()   # 저장
        return redirect("/cart_list")   # 장바구니 목록으로 이동

    else:   # 세션이 없으면(로그인하지 않은 경우)
        return redirect("/login")   # 로그인 페이지로 이동

# 장바구니 개별삭제(http://localhost/cart_del?cart_id=장바구니코드)
@csrf_exempt
def cart_del(request):
    # 클릭한 상품의 장바구니 코드에 해당하는 레코드가 삭제됨
    Cart.objects.get(cart_id=request.GET["cart_id"]).delete()
    # 장바구니 목록을 이동
    return redirect("/cart_list")

# 장바구니 비우기(http://localhost/cart_del_all)
@csrf_exempt
def cart_del_all(request):
    # 세션변수 체크
    uid = request.session.get("userid", "")
    if uid != "": # 세션이 존재하면(로그인한 상태)
        # 장바구니 비우기 실행
        Cart.objects.filter(userid = uid).delete()
        # 장바구니 목록으로 이동
        return redirect("/cart_list")
    else:   # 세션이 없으면(로그인하지 않은 상태)
        # 로그인 페이지로 이동
        return redirect("/login")