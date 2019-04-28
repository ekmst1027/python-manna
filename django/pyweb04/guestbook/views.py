from django.shortcuts import render, render_to_response, redirect
from guestbook.models import Guestbook
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

# 방명록 리스트(http://localhost)
@csrf_exempt
def list(request):
    try:
        msg = request.GET["msg"]
    except:
        msg = ""

    # 검색 옵션
    try:
        searchkey = request.POST["searchkey"]
    except:
        searchkey = "name" # 검색 옵션 기본값
    # 검색 키워드
    try:
        search = request.POST["search"]
    except:
        search = "" # 검색 키워드 기본값

    # gbCount = Guestbook.objects.count()
    # 필드명__contains = 검색어
    # ex) name__contains='kim' => WHERE name like '%kim%'
    if searchkey == "name_countent":
        gbCount = Guestbook.objects.filter(\
            Q(name__contains = search) | Q(content__contains = search)).count()
    elif searchkey == "name":
        gbCount = Guestbook.objects.filter(\
            name__contains = search).count()
    elif searchkey == "content":
        gbCount = Guestbook.objects.filter(\
            content__contains = search).count()

    # gbList = Guestbook.objects.order_by("-idx")[:]
    if searchkey == "name_content":
        gbList = Guestbook.objects.filter(\
            Q(name__contains = search) | \
            Q(content__contains=search)).order_by("-idx")
    elif searchkey == "name":
        gbList = Guestbook.objects.filter(\
            name__contains = search).order_by("-idx")
    elif searchkey == "content":
        gbList = Guestbook.objects.filter(\
            content__contains = search).order_by("-idx")

    # list.html 페이지로 넘어가서 출력됨
    return render_to_response(\
        "list.html", {"gbCount":gbCount, "gbList":gbList, \
            "searchkey": searchkey, "search": search, "msg": msg})


def write(request):
    return render_to_response("write.html")

@csrf_exempt # 크로스 사이트 스크립팅 공격을 방지하기 위한 코드
def insert(request):
    # 사용자가 입력한 내용을(post 방식으로 넘어온 값들) 객체에 저장
    vo = Guestbook(name=request.POST["name"],
                    email=request.POST["email"],
                    passwd=request.POST["passwd"],
                    content=request.POST["content"])
    # insert query가 호출됨
    vo.save()
    # http://localhost로 이동(목록이 갱신됨)
    return redirect("/")

@csrf_exempt
def passwd_check(request):
    id = request.POST["idx"]    # 글번호
    pwd = request.POST["passwd"]    # 사용자가 입력한 비밀번호
    vo = Guestbook.objects.get(idx=id)  # 원글을 읽음
    # 원글의 비번과 사용자가 입력한 비번이 같으면
    if vo.passwd == pwd:
        # 수정 페이지로 이동
        return render_to_response("edit.html", {"vo":vo})
    else:   # 비번이 틀리면 목록으로 되돌아감
        return redirect("/?msg=error")

# 방명록 수정(http://localhost/gb_update)
@csrf_exempt
def update(request):
    # 수정할 게시물 번호
    id = request.POST["idx"]
    # 수정할 내용을 Guestbook 객체에 저장
    vo = Guestbook(idx = id,
                    name = request.POST["name"],
                    email = request.POST["email"],
                    passwd = request.POST["passwd"],
                    content = request.POST["content"])
    # update query가 호출됨
    vo.save()
    # 목록으로 이동
    return redirect("/")

@csrf_exempt
def delete(request):
    # 삭제할 글번호
    id = request.POST["idx"]
    # 삭제할 레코드를 조회한 후 삭제 처리
    Guestbook.objects.get(idx=id).delete()
    # 목록으로 이동
    return redirect("/")