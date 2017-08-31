import os
import re
import time
import getpass
import readline
import django
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openergate.settings")
django.setup()
from django.core.management import execute_from_command_line
from django.contrib.auth.models import User
from django.conf import settings
from core.models import *

#创建管理员
User.objects.create_superuser('admin', 'admin@example.com', 'password', last_name='admin')

#初始化特定角色
init_role_list = [
    {'name':'user_role_admin','zh_name':'用户角色管理员'}, 
    {'name':'workflow_admin','zh_name':'工作流管理员'}, 
    {'name':'workflow_supervisor','zh_name':'工作流督办员'}, 
    {'name':'ldap_admin','zh_name':'LDAP管理员'}, 
    {'name':'mtree_admin', 'zh_name':'业务树管理员'},
    {'name':'op', 'zh_name':'运维人员'},
    {'name':'dba', 'zh_name':'数据库管理员'},
]
if Role.objects.count() == 0:
    for role in init_role_list:
        Role.objects.create(name=role['name'], zh_name=role['zh_name'], desc=role['zh_name'], creator='root', flag=1)

