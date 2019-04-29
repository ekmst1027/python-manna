from django.shortcuts import render, render_to_response
from .models import Product

# 시작 페이지(http://localhost)
def home(request):
    # index.html로 이동
    return render(request, "index.html")

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