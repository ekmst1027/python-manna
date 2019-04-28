from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from survey.models import Survey, Answer

# 시작페이지(http://localhost)
def main(request):
    # Survey.objects 모든 레코드, filter 조건(where절에 해당)
    # order_by 필드명 앞에 - => 내림차순
    survey = Survey.objects.filter(status="y").order_by("-survey_idx")[0]
    #main.html로 포워딩
    return render_to_response("main.html", {"survey" : survey})

# 설문응답을 저장하는 코드(http://localhost/save_survey)
@csrf_exempt
def save_survey(request):
    # 문제 번호와 응답번호를 Answer 객체에 저장
    vo = Answer(survey_idx = request.POST["survey_idx"],
                num = request.POST["num"])
    # insert query가 호출됨
    vo.save()
    # success.html로 이동
    return render_to_response("success.html")

def show_result(request):
    # 문제 번호
    idx = request.GET['survey_idx']
    # SELECT * FROM survey WHREE survey_idx = 1
    ans = Survey.objects.get(survey_idx=idx)
    answer = [ans.ans1, ans.ans2, ans.ans3, ans.ans4]
    # Survey.objects.raw() : sql 문장 자체를 실행
    surveyList = Survey.objects.raw("""
    SELECT
        survey_idx, num, count(num) sum_num,
        ROUND((SELECT COUNT(*) FROM survey_answer
                WHERE survey_idx = a.survey_idx and num = a.num) * 100.0 /
                (SELECT COUNT(*) FROM survey_answer WHERE survey_idx = a.survey_idx), 1) rate
    FROM survey_answer a
    WHERE survey_idx = %s
    GROUP BY survey_idx, num
    ORDER BY num
    """, idx)

    surveyList = zip(surveyList, answer)

    return render_to_response("result.html", {"surveyList" : surveyList})