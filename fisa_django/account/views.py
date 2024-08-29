from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# Create your views here.
def user_login(request):
    if request.method == 'POST':

        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    response = HttpResponse('인증 성공')
                    response.set_cookie('user', user)
                    response.set_cookie('testCookie', 'value testCookie')
                    response.content = f"로그인 되었습니다! {request.COOKIES.get('user'), request.COOKIES.get('testCookie')}"

                    request.session['testSession'] = 'value session'

                    response.content =f'로그인 되셨습니다! {request.COOKIES.get("user"), request.COOKIES.get("testCookie")} \n session: {request.session.get("testSession")} '


                    return response
                else:
                    return HttpResponse('사용불가')
            else:
                return HttpResponse('로그인 정보가 틀립니다.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

