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
def list(request):
    # 레코드 갯수
    boardCount = Board.objects.count()
    # 글번호 내림차순으로 게시물 리스트를 받음
    boardList = Board.objects.all().order_by("-idx")
    # list.html로 포워딩하여 출력됨
    return render_to_response("list.html",
        {"boardList": boardList, "boardCount": boardCount})

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
