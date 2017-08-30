from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def add_task(request):
    title,title_list = '新建事项','新建事项列表'
    return render_to_response('workflow/add_task.html',locals())
@login_required
def waiting_task(request):
    title,title_list = '待办事项','待办事项列表'
    return render_to_response('workflow/waiting_task.html',locals())
@login_required
def done_task(request):
    title,title_list = '已办事项','已办事项列表'
    return render_to_response('workflow/done_task.html',locals())
@login_required
def sent_task(request):
    title,title_list = '已发事项','已发事项列表'
    return render_to_response('workflow/sent_task.html',locals())
@login_required
def supervisor_task(request):
    title,title_list = '督办事项','督办事项'
    return render_to_response('workflow/supervisor_task.html',locals())
@login_required
def all_task(request):
    title,title_list = '所有事项','所有事项列表'
    return render_to_response('workflow/all_task.html',locals())
@login_required
def order_list(request):
    title,title_list = '工作流管理','工作流管理列表'
    return render_to_response('workflow/order_list.html',locals())
