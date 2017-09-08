"""openergate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from workflow.views import *


urlpatterns = [
    url(r'^$', link_task, name='link_task'),
    url(r'^add_order/$', add_order, name='add_order'),
    url(r'^edit_order/$', edit_order, name='edit_order'),
    url(r'^link_task/$', link_task, name='link_task'),
    url(r'^waiting_task/$', waiting_task, name='waiting_task'),
    url(r'^done_task/$', done_task, name='done_task'),
    url(r'^sent_task/$', sent_task, name='sent_task'),
    url(r'^supervisor_task/$', supervisor_task, name='supervisor_task'),
    url(r'^all_task/$', all_task, name='all_task'),
    url(r'^add_task/$', add_task, name='add_task'),
    url(r'^order_list/$', order_list, name='order_list'),
    url(r'^ajax_task$', ajax_task, name='ajax_task'),
    url(r'^ajax_order$', ajax_order, name='ajax_order'),

#------------申请类型---------------
    url(r'^server_ask/$', server_ask, name='server_ask'),
]
