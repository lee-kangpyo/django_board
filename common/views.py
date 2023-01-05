from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from common.forms import UserForm


def signup(request):
    if request.method == "POST":
        #POST 요청의 경우 입력된 데이터로 사용자를 생성
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)           # 사용자 인증
            login(request, user)                                                    # 로그인
            return redirect('index')
    else:
        # GET요청의 경우는회원 가입 화면을 보여줌.
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})