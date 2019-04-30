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
    # 상품 등록(http://localhost/product_write)
    path('product_write', views.product_write),
    # 상품 저장(http://localhost/product_insert)
    path('product_insert', views.product_insert), 
    # 상품 수정폼(http://localhost/product_edit?product_id=6)
    path('product_edit', views.product_edit), 
    # 상품정보 수정(http://localhost/product_update)
    path('product_update', views.product_update), 
    # 상품정보 삭제(http://localhost/product_delete)
    path('product_delete', views.product_delete), 

]
