from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template.defaulttags import register
from django.contrib.auth.models import User
from django.db.models import Q
from workflow.models import Task, Task_log, Work_order
from core.models import *
from django.conf import settings
# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def require_role(role_list=[]):
    def _deco(func):
        def __deco(request,*args,**kwargs):
            roles = []
            user = request.user
            roles = [row.name for row in user.role_set.all()]
            if user.is_superuser:
                roles.append('superuser')
            allow_list = list(set(role_list).intersection(set(roles)))
            if not allow_list:
                return HttpResponse('无权限访问')
            return func(request,*args,**kwargs)
        return __deco
    return _deco

def get_roles_by_username(username):
    user = User.objects.get(username=username)
    roles = [row.name for row in user.role_set.all()]
    if user.is_superuser:
        roles.append('superuser')
    return roles

def get_role_name():
    roles = Role.objects.all()
    role_dict = {}
    role_dict[0] = "发起人确认"
    for role in roles:
        role_dict[role.id] = role.zh_name
    return role_dict

@login_required
def index(request):
    user = request.user
    username = user.username
    usermail = user.email
    is_superuser = user.is_superuser
    if 'modename' in request.session:
        modename = request.session['modename']
    else:
        # 登陆默认页为待处理工单
        request.session['modename'] = modename = 'workflow/waiting_task'
    # workflow
    roles = get_roles_by_username(username)
    if 'op' in roles: 
        is_op = 1
    if 'user_role_admin' in roles: 
        is_user_role_admin = 1
    if 'workflow_admin' in roles: 
        is_workflow_admin = 1
    if 'workflow_supervisor' in roles:
        is_workflow_supervisor = 1
    if 'superuser' in roles:
        is_user_role_admin = is_workflow_admin = is_workflow_supervisor = is_op = 1
    task_num_dict = {}
    task_id_list = [ row.task_id for now in Task_log.objects.filter(username=username).distinct()]
    task_num_dict['done_num'] = Task.objects.filter(id__in=task_id_list).count()
    task_num_dict['waiting_num'] = Task.objects.filter(Q(cur_users__contains=username+';')|Q(cur_user=username)).count()
    task_num_dict['all_num'] = Task.objects.all().count()
    task_num_dict['sent_num'] = Task.objects.filter(creator=username).count()
    task_num_dict['supervisor_num'] = Task.objects.filter(Q(state=2)|Q(state=3)).count()
    return render_to_response('core/index.html',locals())

# role
@login_required
@require_role(role_list=['user_role_admin','superuser'])
def add_role(request):
    title = '添加角色'
    users = User.objects.all()
    return render_to_response('core/add_role.html',locals())

@login_required
@require_role(role_list=['user_role_admin','superuser'])
def edit_role(request):
    title = '编辑角色'
    id = request.GET.get('id').strip()
    if id:
        users = User.objects.all()
        ret = Role.objects.get(id=int(id))
    else:
        return HttpResponse('参数错误')
    return render_to_response('core/edit_role.html',locals())
def role_list(request):
    title,title_list = '系统角色','系统角色列表'
    key = request.GET.get('key','').strip()
    #key = request.user
    print ('key:',key)
    rets = Role.objects.all()
    if key:
        rets = Role.objects.filter(Q(name__contains=key)|Q(zh_name__contains=key)|Q(desc__contains=key))
    msgnum = rets.count()
    return render_to_response('core/role_list.html',locals())

@login_required
def get_role_user(request):
    users = []
    role_name = request.GET.get('role_name').strip()
    try:
        role = Role.objects.get(name=role_name)
    except:
        return HttpResponse('角色名不存在')
    users = role.users.all()
    users = [row.username for row in users]
    return HttpResponse(json.dumps(users))

@login_required
def get_user_roles(request):
    user = request.user
    roles = [row.name for row in user.role_set.all()]
    if user.is_superuser:
        roles.append('superuser')
    return HttpResponse(json.dumps(roles))






