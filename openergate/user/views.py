from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
# Create your views here.

# 登陆
def login(request):
    next_url = request.GET.get('next')
    if next_url == None:
        next_url = "/"    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        if user is None:
            passwd_err = '用户名或密码错误！'
        else:
            auth.login(request,user)
            return HttpResponseRedirect(next_url)
    return render_to_response('core/login.html')

@login_required
def test(request):
    return HttpResponse('ok')
