from django.db import models

# Create your models here.
class Work_order(models.Model):
    '''工单表'''
    name = models.CharField('工单名(英文)',max_length=30,unique=True)
    title = models.CharField('标题',max_length=30)
    desc = models.TextField('描述', blank=True)
    flow = models.CharField('流程',max_length=10,blank=True)
    take_time = models.IntegerField('操作需要时间',default=1, blank=True)
    is_active = models.IntegerField('是否启用',default=1)
    creator = models.CharField('创建人',max_length=30)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)

class Task(models.Model):
    '''任务表'''
    title = models.CharField('标题',max_length=30)
    creator = models.CharField('创建人',max_length=30)
    work_order_id = models.IntegerField('工单id')
    flow = models.CharField('流程',max_length=10,blank=True)
    data = models.CharField('表单提交数据',max_length=999)
    state = models.IntegerField('当前状态',default=1)
    cur_role_id = models.IntegerField('当前处理角色id')
    cur_users = models.CharField('当前可处理人列表',max_length=999,blank=True)
    cur_user = models.CharField('当前处理人',max_length=30, blank=True)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)

class Task_log(models.Model):
    task_id = models.IntegerField('任务id')
    username = models.CharField('用户名',max_length=30)
    role_id = models.IntegerField('角色id')
    act_type = models.IntegerField('处理类型', default=1)
    act_opinion = models.TextField('处理意见反馈', blank=True,max_length=1000)
    create_time = models.DateTimeField('记录时间',auto_now_add=True) 
