# from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm


def index(request):
    # 단순하게 문자열을 브라우저에 출력
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    question_list = Question.objects.order_by("-create_date")
    obj = {'question_list':question_list}
    return render(request, 'pybo/question_list.html', obj)


def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    obj = {"question":question}
    return render(request, 'pybo/question_detail.html', obj)


def answer_create(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # 아래코드로 저장도 가능 Answer 클래스 import 필요
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()QuestionForm

    return redirect("pybo:detail", question_id=question.id)


def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)


    #return render(request, 'pybo/question_form.html', {"form" : form})