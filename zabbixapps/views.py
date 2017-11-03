#coding:utf-8

from django.http import HttpResponse
from django.shortcuts import render
from pprint import pprint

from .zabbixtools import Zabbixtools
from .forms import CreateHostAddForm
from .forms import DelHostAddForm

host = Zabbixtools()
def create_host(request):
    #当提交表单时使用POST方式
    if request.method == 'POST':
        #form包含提交的数据
        form = CreateHostAddForm(request.POST)
        #如果提交的数据合法
        if form.is_valid():
            a = form.cleaned_data['ip']
            b = form.cleaned_data['groupids']
            c = form.cleaned_data['templateids']
            # pprint(a)
            # return HttpResponse(str(int(a))
            create_host_message = host.host_create(a, b, c)
            # pprint(create_host_message)
            return HttpResponse(create_host_message)
    else:
        form = CreateHostAddForm()
    return render(request, 'zabbixapps/host_manage.html', {'form':form})

def del_host(request):
    if request.method == 'POST':
        form = DelHostAddForm(request.POST)
        if form.is_valid():
            a = form.cleaned_data['ip']
            del_host_message = host.host_del(a)
            pprint(del_host_message)
            return HttpResponse(del_host_message)
    else:
        form = DelHostAddForm()
    return  render(request, 'zabbixapps/host_manage.html', {'form': form})


def get_host(request):
    host_list = host.host_get()
    # pprint(host_list)
    # for item in host_list:
    #      item['interfaces'] = item['interfaces'][0]['ip']
    # pprint(host_list)

    # return HttpResponse(host_list)
    return render(request, 'zabbixapps/host_list.html', {'host_list':host_list})

def get_template(request):
    template_list = host.template_get()
    # pprint(template_list)
    # return  HttpResponse(template_list)
    return render(request, 'zabbixapps/template_list.html', {'template_list': template_list})

def get_hostgroup(request):
    hostgroup_list = host.hostgroup_get()
    # pprint(hostgroup_list)
    # return HttpResponse(hostgroup_list)
    return render(request, 'zabbixapps/hostgroup_list.html', {'hostgroup_list': hostgroup_list})


def echarts(request):
    return render(request,'echarts.html')

def index(request):
    return render(request, 'index.html')