from django.contrib import admin
from django.conf import settings
from django.conf.urls import include, url  # For django versions before 2.0
from django.urls import include, path  # For django versions from 2.0 and up
from survey import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # 시작페이지 
    url(r'^$', views.main),  
    # 설문내용 저장(http://localhost/save_survey)
    url(r'^save_survey$', views.save_survey),
    # 설문결과 보기(http://localhost/show_result)
    url(r'^show_result$', views.show_result), 
]

# 디버깅 관련 url
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls))
    ]