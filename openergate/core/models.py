from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Role(models.Model):
    name = models.CharField('角色名',max_length=50,unique=True)
    zh_name = models.CharField('角色中文名',max_length=100)
    desc = models.CharField('角色权限说明',max_length=500,blank=True)
    flag = models.IntegerField('标志',default=0)
    creator = models.CharField('创建人',max_length=30,blank=True)
    users = models.ManyToManyField(User,blank=True)
    create_time = models.DateTimeField('创建时间',auto_now_add=True)
    update_time = models.DateTimeField('更新时间',auto_now=True)
