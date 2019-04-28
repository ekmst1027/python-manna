import math
import os
from django.shortcuts import render, redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from board.models import Board, Comment
from django.utils.http import urlquote

# 파일이 업로드될 디렉토리 지정
UPLOAD_DIR = "/Users/kyeongmin/Documents/python_basic/upload/"

# 게시물 목록(http://localhost)
@csrf_exempt
def list(request):
    # 검색옵션
    try:
        search_option = request.POST["search_option"]
    except:
        search_option = "writer" # 검색옵션 기본값

    # 검색키워드
    try:
        search = request.POST["search"]
    except:
        search = ""

    if search_option == "all":
        boardCount = Board.objects.filter(\
        Q(writer__contains=search) | Q(title__contains=search) | Q(content__contains=search)).count()
    elif search_option == "writer":
        boardCount = Board.objects.filter(writer__contains = search).count()
    elif search_option == "title":
        boardCount = Board.objects.filter(title__contains = search).count()
    elif search_option == "content":
        boardCount = Board.objects.filter(content__contains = search).count()

    try:
        start = int(request.GET["start"])
    except:
        start = 0

    page_size = 10  # 페이지당 게시물수
    page_list_size = 10 # 한 화면에 표시할 페이지의 갯수
    end = start + page_size
    total_page = math.ceil(boardCount / page_size)
    current_page = math.ceil( (start+1) / page_size )
    start_page = \
        math.floor((current_page - 1) / page_list_size) * page_list_size + 1
    end_page = start_page + page_list_size - 1
    if total_page < end_page:
        end_page = total_page
    if start_page >= page_list_size:
        prev_list = (start_page - 2) * page_size
    else:
        prev_list = 0
    if total_page > end_page:
        next_list = end_page * page_size
    else:
        next_list = 0
    print("start : ", start)
    print("end : ", end)
    print("startpage : ", start_page)
    print("endpage : ", end_page)
    print("search:",search)
    print("searchoption:",search_option)

    if search_option == "all":
        boardList = Board.objects.filter(\
            Q(writer__contains=search) | Q(title__contains=search) | \
            Q(content__contains=search)).order_by("-idx")[start:end]
    elif search_option == "writer":
        boardList = Board.objects.filter(\
            writer__contains=search).order_by("-idx")[start:end]
    elif search_option == "title":
        boardList = Board.objects.filter(\
            title__contains=search).order_by("-idx")[start:end]
    elif search_option == "content":
        boardList = Board.objects.filter(\
            content__contains=search).order_by("-idx")[start:end]

    links = []
    for i in range(start_page, end_page+1):
        page = (i - 1) * page_size
        links.append("<a href='?start="+str(page)+"'>"+str(i)+"</a>")
    print("links : ", links)

    print("boardList")
    print(boardList)

    return render_to_response("list.html",
        {"boardList": boardList, "boardCount": boardCount,
        "search_option": search_option, "search": search,
        "range":range(start_page-1, end_page),
        "start_page": start_page, "end_page": end_page,
        "page_list_size": page_list_size,
        "total_page": total_page, "prev_list": prev_list,
        "next_list": next_list, "links": links})

# 글쓰기 페이지로 이동(http://localhost/write)
def write(request):
    return render_to_response("write.html")

# 글저장(http://localhost)
@csrf_exempt
def insert(request):
    # 파일 업로드 작업
    fname = ""
    fsize = 0
    # 업로드된 파일이 있으면
    if "file" in request.FILES:
        # <input type="file">태그의 name
        file = request.FILES["file"]
        # 첨부파일의 이름
        fname = file._name

        # wb : 이진파일 쓰기 모드
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        # 파일을 몇개의 뭉치로 나눠서 저장
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        # 첨부파일의 크기(업로드 완료 후 계산)
        fsize = os.path.getsize(UPLOAD_DIR+fname)

    vo = Board(writer = request.POST["writer"],
                title = request.POST["title"],
                content = request.POST["content"],
                filename = fname,
                filesize = fsize)

    # insert query가 실행됨
    vo.save()
    # django의 콘솔에 출력됨
    print(vo)
    # 목록으로 이동
    return redirect("/")

def download(request):
    # 게시물 번호
    id = request.GET['idx']
    # 게시물 번호에 해당하는 레코드 선택
    vo = Board.objects.get(idx=id)
    # 첨부파일의 전체 경로
    path = UPLOAD_DIR + vo.filename
    print("path :", path)
    # 디렉토리를 제외한 파일의 이름
    filename = os.path.basename(path)
    # 파일이름의 인코딩 방식
    # filename = filename.encode("utf-8")
    # url에 포함된 특수문자 처리
    filename = urlquote(filename)
    print("pfilename:", os.path.basename(path))
    # 파일 오픈
    with open(path, 'rb') as file:
        # 서버의 파일을 읽음, 파일 종류가 다양하므로 octet-stream으로 선언
        response = HttpResponse(file.read(), content_type="application/octet-stream")

        # 첨부파일의 이름(한글 파일 일므이 깨지지 않도록 처리)
        response["Content-Disposition"] = \
            "attachment; filename*=UTF-8''{0}".format(filename)

        # 다운로드 횟수 1증가 처리
        vo.down_up()

        # update 쿼리가 실행됨
        vo.save()

        # 첨부파일을 클라이언트로 전송
        return response

# 상세화면(http://localhost/detail)
def detail(request):
    try:
        search_option = request.GET["search_option"]
    except:
        search_option = "writer"
    try:
        search = request.GET["search"]
    except:
        search = ""

    # 클릭한 글번호
    id = request.GET["idx"]
    # 글번호에 해당하는 레코드 선택
    vo = Board.objects.get(idx=id)
    # 조회수 증가 처리
    vo.hit_up()
    vo.save()
    # 첨부파일의 크기
    filesize = "%.2f" % (vo.filesize / 1024)
    # 댓글 목록
    commentList = Comment.objects.filter(board_idx=id).order_by("idx")

    # detail.html로 넘어가서 출력됨
    return render_to_response("detail.html",
            {"vo": vo, "filesize": filesize, "commentList": commentList,
            "search_option": search_option, "search": search})

# 댓글 저장(http://localhost/reply_insert)
@csrf_exempt
def reply_insert(request):
    # 게시물 번호
    id = request.POST["idx"]
    # 댓글 객체 생성
    vo = Comment(board_idx= id,
                writer = request.POST["writer"],
                content = request.POST["content"])

    # insert query가 호출됨
    vo.save()
    # 상세화면으로 다시 돌아감
    return HttpResponseRedirect("detail?idx="+id)

# 글 수정(http://localhost/update)
@csrf_exempt
def update(request):
    # 글번호
    id = request.POST["idx"]
    # 수정 전의 레코드 조회
    vo_src = Board.objects.get(idx=id)
    # 수정 전의 첨부파일이름과 사이즈
    fname = vo_src.filename
    fsize = vo_src.filesize

    # 새로운 첨부파일이 있으면
    if "file" in request.FILES:
        # <input type="file" 태그의 name이 file인 태그
        file = request.FILES["file"]
        # 업로드한 파일의 이름
        fname = file._name
        # wb : write binary
        fp = open("%s%s" % (UPLOAD_DIR, fname), "wb")
        # 파일 조각들을 조금씩 저장
        for chunk in file.chunks():
            fp.write(chunk)
        # 파일 닫기
        fp.close()

        # 첨부파일의 크기(업로드 완료 후 계산)
        fsize = os.path.getsize(UPLOAD_DIR+fname)

    # 수정 후의 내용
    vo_new = Board( idx = id,
                    writer = request.POST["writer"],
                    title = request.POST["title"],
                    content = request.POST["content"],
                    filename = fname,
                    filesize = fsize)

    # update 쿼리가 호출됨
    vo_new.save()

    # 시작 페이지로 이동
    return redirect("/")

# 파일 삭제(http://localhost/delete)
@csrf_exempt
def delete(request):
    # 글번호
    id = request.POST["idx"]
    # 레코드 삭제
    Board.objects.get(idx=id).delete()
    # 시작 페이지로 이동
    return redirect("/")