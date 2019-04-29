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
]
