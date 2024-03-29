# from django.http import HttpResponse

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

def index(request):
    # 단순하게 문자열을 브라우저에 출력
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    page = request.GET.get("page", '1')                         # 키값 페이지에 해당하는 값을 가져온다. 기본값:1
    question_list = Question.objects.order_by("-create_date")
    paginator = Paginator(question_list, 10)                    # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    obj = {'question_list':page_obj}
    return render(request, 'pybo/question_list.html', obj)


def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    obj = {"question":question}
    return render(request, 'pybo/question_detail.html', obj)

@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''
    답변등록    
    '''
    question = get_object_or_404(Question, id=question_id)
    
    # request로 질문 객체 만드는 3가지
    # question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    # 아래코드로 저장도 가능 Answer 클래스 import 필요
    # answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
    # answer.save()

    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user   # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)


@login_required(login_url='common:login')
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form':form}
    return render(request, 'pybo/question_form.html', context)
    #return render(request, 'pybo/question_form.html', {"form" : form})