from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from core.views import *
from core.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@register.filter
def get_flow_names(flow):
    flow_names = '免审批'
    flow_id_list = flow.split('-')
    if flow_id_list[0]:
        flow_name_list = [Role.objects.get(id=role_id).zh_name for role_id in flow_id_list]
        flow_names = '->'.join(flow_name_list)
    return flow_names

@login_required
#@require_role(role_list=['workflow_admin'])
def add_order(request):
    title = '添加工作流'
    username = request.user.username
    roles = Role.objects.all()
    return render_to_response('workflow/add_order.html',locals())

@login_required
def link_task(request):
    title,title_list = '新建事项','新建事项列表'
    username = request.user.username
    rets = Work_order.objects.filter(is_active=1)
    return render_to_response('workflow/link_task.html',locals())

@login_required
def server_ask(request):
    title,title_user,title_text = '服务器类','申请人信息','申请服务器设备'
    return render_to_response('workflow/server_ask.html',locals())


@login_required
def add_task(request):
    title = '新建事项'
    #查看工单必须包含id参数
    work_order_id = request.GET.get('order_id','').strip()
    task_id = request.GET.get('id','').strip()
    #这两个参数有且只有一个
    if (not work_order_id and not task_id) or (work_order_id and task_id): return HttpResponse('参数错误')
    user = request.user
    username = creator = user.username
    #只有order_id参数为添加工单
    if work_order_id: work_order_id = int(work_order_id)
    #只有id参数为编辑工单
    if task_id:
        task_id = int(task_id)
        ret = Task.objects.get(id=task_id)
        creator = ret.creator
        state = ret.state
        work_order_id = ret.work_order_id
        if creator != username: return HttpResponse('您不是本工单任务创建人')
        if state != 1: return HttpResponse('工单已处理')
        data = json.loads(ret.data)
        task_log = Task_log.objects.filter(task_id=task_id).order_by('-create_time')
    work_order_info = Work_order.objects.get(id=work_order_id)
    work_order_flow = work_order_info.flow
    if work_order_flow:
        next_role_id = int(work_order_flow.split('-')[0])
    else:
        next_role_id = 0
    work_order_title = work_order_info.title
    work_order_name = work_order_info.name
    #根据template_name名指定引用的form表单模板
    template_name = 'workflow/%s_form.html' % work_order_name
    display_submit = 1
    if next_role_id != 0:
        next_users = Role.objects.get(id=next_role_id).users.all()
    else:
        next_users = [user]
    role_dict = get_role_name()
    act_type_dict = settings.ACT_TYPE_DICT
    #工单form表单数据定义,新增工作流在此处添加表单数据
    if work_order_name == 'cicd':
        envs = ['deva', 'devb', 'devc', 'devd', 'deve', 'betaa', 'betab', 'betac', 'betad', 'grey', 'prod', 'android', 'ios']
    return render_to_response('workflow/add_task.html', locals())
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
    title = '工作流列表'
    username = request.user.username
    key = request.GET.get('key','').strip()
    if key:
        rets = Work_order.objects.filter(Q(name__contains=key)|Q(title__contains=key)|Q(desc__contains=key)|Q(creator__contains=key))
    else:
        rets = Work_order.objects.order_by('-id')
    msgnum = rets.count()
    return render_to_response('workflow/order_list.html',locals())
@login_required
#@require_role(role_list=['workflow_admin'])
def edit_order(request):
    title = '编辑工作流'
    username = request.user.username
    roles = Role.objects.all()
    id = request.GET.get('id','').strip()
    if not id: return HttpResponse('参数错误')
    try:
        ret = Work_order.objects.get(id=int(id))
    except:
        return HttpResponse('id不存在')
    if ret.flow:
        role_ids = [int(row) for row in ret.flow.split('-')]
    else:
        role_ids = []
    return render_to_response('workflow/edit_order.html',locals())

@login_required
#@require_role(role_list=['workflow_admin'])
def ajax_order(request):
    username = request.user.username
    if request.method == 'POST':
        result = False
        act = request.POST.get('act','').strip()
        if act == 'add':
            name = request.POST.get('name','').strip()
            if Work_order.objects.filter(name=name): return HttpResponse('工单名已存在')
            title = request.POST.get('title','').strip()
            desc = request.POST.get('desc','')
            is_active = int(request.POST.get('is_active',''))
            flow = request.POST.get('flow','')
            ret = Work_order.objects.create(name=name, title=title, desc=desc, flow=flow, creator=username, is_active=is_active)
            if ret:
                result = '添加成功'
                templates_dir = "%s/templates/workflow" % settings.BASE_DIR
                scripts_dir = "%s/workflow/scripts" % settings.BASE_DIR
                os.system("cd %s;test -f %s_form.html || \cp demo_form.html %s_form.html" % (templates_dir, name, name))
                os.system("cd %s;test -f %s.sh || \cp demo.sh %s.sh" % (scripts_dir, name, name))
        elif act == 'edit':
            name = request.POST.get('name','').strip()
            title = request.POST.get('title','').strip()
            desc = request.POST.get('desc','')
            is_active = int(request.POST.get('is_active',''))
            flow = request.POST.get('flow','')
            ret = Work_order.objects.filter(name=name).update(title=title, desc=desc, flow=flow, creator=username, is_active=is_active)
            if ret: result = '修改成功'
        elif act == 'del':
            id = request.POST.get('id','').strip()
            order_obj = Work_order.objects.filter(id=id)
            ret = order_obj.delete()
            if ret: result = '删除成功'
    return HttpResponse(result) 
@login_required
def ajax_task(request):
    user = request.user
    username = user.username
    is_supervisor = 0
    #判断是否有督办权限
    roles = [row.name for row in user.role_set.all()]
    if 'workflow_supervisor' in roles: 
        is_supervisor = 1
        admin_role_id = Role.objects.get(name='workflow_supervisor').id
    if request.method == 'POST':
        act = request.POST.get('act','').strip()
        #提交工单
        if act == 'add':
            task_id = request.POST.get('task_id','').strip()
            creator = request.POST.get('creator','').strip()
            creator_name = user.last_name
            creator_mail = user.email
            next_role_id = int(request.POST.get('next_role_id').strip())
            next_user = request.POST.get('next_user','').strip()
            work_order_id = int(request.POST.get('work_order_id').strip())
            #从POST数据中提取form表单中数据
            data = request.POST.lists()
            data = dict(data)
            #删除垃圾数据，保留重要表单中有用的数据
            data.pop('act')
            data.pop('task_id')
            data.pop('creator')
            data.pop('next_role_id')
            if data.has_key('next_user'): 
                data.pop('next_user')
                next_user, next_user_mail = next_user.split('_')
            data.pop('work_order_id')
            work_order_obj = Work_order.objects.get(id=work_order_id)
            work_order_title = work_order_obj.title
            work_order_name = work_order_obj.name
            flow = work_order_obj.flow
            title = creator_name + work_order_title
            #免审批流程
            if next_role_id == 0:
                next_state = 4
                next_users = creator + ';'
                data = json.dumps(data)
                ret = Task.objects.create(title=title, creator=creator, work_order_id=work_order_id, flow=flow,
                    data=data, state=next_state, cur_role_id=next_role_id, cur_users=next_users, cur_user='')
                task_id = ret.id
                exec_task.delay(task_id)
                result = '免审批工单已提交'
            #审批流程
            else:    
                next_state = 2
                next_users = Role.objects.get(id=next_role_id).users.all()
                next_users = [row.username for row in next_users]
                next_users = ';'.join(next_users) + ';'
                #业务树权限管理有独立的角色管理，忽略工作流中的角色
                if work_order_name == 'mtree_role': next_users = data.pop('users')[0]
                data = json.dumps(data)
                #工单被驳回修改后提交有task_id参数
                if task_id:
                    task_id = int(task_id)
                    Task.objects.filter(id=task_id,state__lte=2).update(title=title, creator=creator, work_order_id=work_order_id, flow=flow,
                        data=data, state=next_state, cur_role_id=next_role_id, cur_users=next_users, cur_user='')
                #全新创建提交工单
                else:
                    ret = Task.objects.create(title=title, creator=creator, work_order_id=work_order_id, flow=flow, 
                        data=data, state=next_state, cur_role_id=next_role_id, cur_users=next_users, cur_user='')
                    task_id = ret.id 
                #给审批人发送工单处理通知
                tolist = [next_user_mail]
                subject = '<%s>工单处理通知' % title
                content = '<br>您好！<br>%s 工单任务已发起，等待您处理，<a href="%s/workflow/edit_task?id=%d" target="_blank">点击此处查看处理</a>，谢谢！' % (title, settings.SYS_API, task_id)
                send_html_mail(tolist, subject, content)
                result = settings.TASK_STATE_DICT[next_state]
        #审批工单
        elif act == 'audit':
            #task_id、act_type和act_opinion是必须参数，act_opinion参数内容可以为空，next_user为可选参数，是当前审批人指定下一位审批人
            task_id  = request.POST.get('task_id','').strip()
            act_type  = request.POST.get('act_type','').strip()
            act_opinion  = request.POST.get('act_opinion','').strip()
            next_user  = request.POST.get('next_user','').strip()
            if not task_id and not act_type: return HttpResponse('参数错误')
            task_id = int(task_id)
            act_type = int(act_type)
            ret = Task.objects.get(id=task_id)
            work_order_id = ret.work_order_id
            title = ret.title
            cur_state = ret.state
            creator = ret.creator
            cur_role_id = ret.cur_role_id
            cur_users = ret.cur_users
            cur_user = ret.cur_user
            user_info = User.objects.get(username=creator)
            creator_name = user_info.last_name
            creator_mail = user_info.email
            flow = ret.flow
            flow_list = flow.split('-')
            #当前审批人是工单申请人时
            if cur_user == creator and cur_state == 4:
                next_role_id = -1
                next_users = next_user = ''
                #撤销
                if act_type == 0: next_state = 0
                #确认
                if act_type == 1: next_state = 5
            #当前审批角色是流程最后一个审批角色时
            elif flow_list.index(str(cur_role_id)) + 1 == len(flow_list):
                #下一个审批角色为申请人
                next_role_id = 0
                #撤销
                if act_type == 0: 
                    next_state = 0
                    next_role_id = -1
                    next_users = next_user = ''
                #同意
                if act_type == 1: 
                    try:
                        exec_task.delay(task_id)
                    except Exception as e:
                        logger.error("rabbitmq error:" + e)
                        return HttpResponse('添加任务报错了')
                    next_state = 4
                    next_user = creator
                    next_users = creator + ';'
                #驳回,申请人重新修改
                if act_type == 2: 
                    next_state = 1
                    next_user = creator
                    next_users = creator + ';'
            #当前审批角色非最后一个审批角色时
            else:
                #撤销
                if act_type == 0:
                    next_role_id = -1
                    next_state = 0
                    next_users = next_user = ''
                #同意
                elif act_type == 1:
                    next_role_id = flow_list[flow_list.index(str(cur_role_id))+1]
                    next_users = Role.objects.get(id=next_role_id).users.all()
                    tolist = [row.email for row in next_users]
                    next_users = [row.username for row in next_users]
                    next_users = ';'.join(next_users) + ';'
                    #只邮件提醒指定的审批人
                    next_user  = request.POST.get('next_user','').strip()
                    if next_user:
                        next_user, next_user_mail = next_user.split('_')
                        tolist = [next_user_mail]
                    #当前审批人为空则未锁定，同一角色成员都能审批
                    next_state = 3
                #驳回
                elif act_type == 2:
                    next_role_id = 0
                    next_state = 1
                    next_user = creator
                    next_users = creator + ';'
            #督办人员
            if username not in cur_users.split(';') and admin_role_id: cur_role_id = admin_role_id
            Task.objects.filter(id=task_id).update(state=next_state, cur_role_id=next_role_id, cur_users=next_users, cur_user='')
            Task_log.objects.create(task_id=task_id,username=username,role_id=cur_role_id,act_type=act_type,act_opinion=act_opinion)
            #邮件通知
            subject = '<%s>工单处理通知' % title
            to_creator_subject = '<%s>工单进度通知' % title
            result = settings.TASK_STATE_DICT[next_state]
            if next_state == 3: 
                content = '<br>您好！<br>%s 工单任务已审批，等待您审批，<a href="%s/workflow/edit_task?id=%d" target="_blank">点击此处查看处理</a>，谢谢！' % (title, settings.SYS_API, task_id)
                #邮件通知下一位审批人处理
                send_html_mail(tolist, subject, content)
                to_creator_content = '<br>您好！<br>%s 工单任务已由%s审批，等待%s审批，<a href="%s/workflow/show_task?id=%d" target="_blank">点击此处查看进度</a>，谢谢！' % (title, cur_user, next_user, settings.SYS_API, task_id)
                #邮件通知申请人进度
                send_html_mail([creator_mail], to_creator_subject, to_creator_content)
            if next_state == 1: 
                result = '已回退'
                to_creator_content = '<br>您好！<br>%s 工单任务已回退，请修改提交，<a href="%s/workflow/add_task?id=%d" target="_blank">点击此处查看处理</a>，谢谢！' % (title, settings.SYS_API, task_id)
                send_html_mail([creator_mail], to_creator_subject, to_creator_content)
            if next_state == 0: 
                to_creator_content = '<br>您好！<br>%s 工单任务已撤销，<a href="%s/workflow/show_task?id=%d" target="_blank">点击此处查看</a>，谢谢！' % (title, settings.SYS_API, task_id)
                send_html_mail([creator_mail], to_creator_subject, to_creator_content)
        else:
            result = '参数错误'
        return HttpResponse(result)
