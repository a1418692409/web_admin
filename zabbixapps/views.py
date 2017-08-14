#coding:utf-8

from django.http import HttpResponse
from django.shortcuts import render
from pprint import pprint

from .zabbixtools import Zabbixtools
from .forms import AddForm


host = Zabbixtools()
def index(request):
    #当提交表单时使用POST方式
    if request.method == 'POST':
        #form包含提交的数据
        form = AddForm(request.POST)
        #如果提交的数据合法
        if form.is_valid():
            a = form.cleaned_data['a']
            # return HttpResponse(str(int(a))
            host.host_create(a)
    else:
        form = AddForm()
    return render(request,'index.html',{'form':form})

def get_host(request):
    # host = zabbixtools()
    host_list = host.host_get()
    # pprint(host_list)
    # for item in host_list:
    #      item['interfaces'] = item['interfaces'][0]['ip']
    # pprint(host_list)

    # return HttpResponse(host_list)
    return render(request, 'host_list.html', {'host_list':host_list})

def get_template(request):
    template_list = host.template_get()
    # pprint(template_list)
    # return  HttpResponse(template_list)
    return render(request, 'template_list.html', {'template_list': template_list})

def get_hostgroup(request):
    hostgroup_list = host.hostgroup_get()
    # pprint(hostgroup_list)
    # return HttpResponse(hostgroup_list)
    return render(request, 'hostgroup_list.html', {'hostgroup_list': hostgroup_list})


def echarts(request):
    return render(request,'echarts.html')