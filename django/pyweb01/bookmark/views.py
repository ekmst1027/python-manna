from django.shortcuts import render, render_to_response
from bookmark.models import Bookmark

# http://localhost 로 요청할 때 실행할 함수(기본 페이지)
def home(request):
    # SELECT * FROM bookmark_bookmark ORDER BY title 쿼리가 실행됨
    urlList = Bookmark.objects.order_by("title")

    # SELECT COUNT(*) FROM bookmark_bookmark 쿼리가 실행됨
    urlCount = Bookmark.objects.all().count()

    # list.html 페이지로 넘어가서 출력됨
    # render_to_response("url", {"변수명" : 값})
    return render_to_response(\
        "list.html", {"urlList": urlList, "urlCount": urlCount})

# http://localhost:detail 로 요청할 때 실행되는 코드
def detail(request):
    # get 방식 변수 받아오기
    addr = request.GET["url"]

    # SELECT * FROM bookmark_bookmark WHERE url=... 실행됨
    vo = Bookmark.objects.get(url=addr)

    # detail.html로 포워딩
    return render_to_response("detail.html", {"vo": vo})