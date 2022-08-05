# Create your views here.

# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Question


def index(request):
    #return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    question_list = Question.objects.order_by("-create_date")
    obj = {'question_list':question_list}
    return render(request, 'pybo/question_list.html', obj)


def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    obj = {"question":question}
    return render(request, 'pybo/question_detail.html', obj)