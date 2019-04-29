from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('admin/', admin.site.urls),
 
    # 시작페이지(http://localhost)
    path('', views.home),
    # 상품목록(http://localhost/product_list)
    path('product_list', views.product_list),
    # 상품상세화면(http://localhost/product_detail)
    path('product_detail', views.product_detail), 
    # 로그인 화면으로 이동(http://localhost/login)
    path('login', views.login_check, name="login"),
    # 회원가입(http://localhost/join)
    path('join/', views.join, name="join"),
    # 로그아웃(http://localhost/logout)
    path('logout/', views.logout, name="logout"),
    # 장바구니 등록(http://localhost/cart_insert)
    path('cart_insert', views.cart_insert),
    # 장바구니 목록(http://localhost/cart_list)
    path('cart_list', views.cart_list),
    # 장바구니 수정(http://localhost/cart_update)
    path('cart_update', views.cart_update),
    # 장바구니 개별삭제(http://localhost/cart_del)
    path('cart_del', views.cart_del),
    # 장바구니 비우기(http://localhost/cart_del_all)
    path('cart_del_all', views.cart_del_all),

]
