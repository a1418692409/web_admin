#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import json
import urllib2
import sys
from pprint import pprint


class Zabbixtools():
    def __init__(self):
        self.url = "https://zabbix.zhbservice.com/zabbix/api_jsonrpc.php"
        self.header = {"Content-Type":"application/json"}
        self.authID = self.user_login()

    def user_login(self):
        data = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"user.login",
                "params":{
                    "user":"Admin",
                    "password":"zhbzabbix",
                },
                "id":0
            }
        )
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            # pprint(result)
        except Exception as e:
            print "Auth Failed, Please Check Your Name And Password:", e
        else:
            response = json.loads(result.read())
            # pprint(response)
            result.close()
            authID = response['result']
            # pprint(authID)
            return authID

    def get_data(self, data):
        request = urllib2.Request(self.url, data)
        # pprint(request)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
            # pprint(result)
        except Exception as e:
            if hasattr(e, 'reason'):
                print "We failed to reach a server."
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())['result']
            result.close()
            # pprint(response)
            return response

    def host_get(self):
        '''
        通过zabbix API获取主机列表
        '''
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "host.get",
                "params": {
                    "output": ["hostid" , "name", "status","host"],
                    "selectInterfaces":["interfaceid",'ip']
                },
                "auth":self.authID,
                "id":1
            }
        )
        # pprint(data)
        # res = self.get_data(data)['result']
        res = self.get_data(data)
        # pprint(res)
        for item in res:
            item['interfaces'] = item['interfaces'][0]['ip']
        # pprint(res)
        return res

    def template_get(self):
        '''
        通过zabbix API获取模板列表
        '''
        data = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"template.get",
                "params":{
                    "output":"extend",
                },
                "auth":self.authID,
                "id":1,
            }
        )
        # res = self.get_data(data)['result']
        res = self.get_data(data)
        # pprint(res)
        return res

    def hostgroup_get(self):
        '''
        通过zabbix API 获取主机组列表
        '''
        data = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"hostgroup.get",
                "params":{
                    "output":"extend",
                },
                "auth":self.authID,
                "id":1,
            }
        )
        res = self.get_data(data)
        # res = json.loads(res)
        pprint(res)
        # res = res['result']
        return res

    def host_del(self):
        '''
        通过zabbix API 删除主机
        '''
        hostip = raw_input('Enter Your Check Host_name: ')
        hostid = self.host_get(hostip)
        if hostid == 0:
            print         "This host cannot find in zabbix,please check it !"
            sys.exit()
        data = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"host.delete",
                "params":[{"hostid": hostid}],
                "auth":self.authID,
                "id":1
            }
        )
        res = self.get_data(data)['result']
        if 'hostids' in res.keys():
            print "\t", "\033[1;32;40m%s\033[0m" % "Delet Host:%s success !" % hostip
        else:
            print "\t", "\033[1;31;40m%s\033[0m" % "Delet Host:%s failure !" % hostip

    def host_create(self):
        '''
        通过zabbix API 添加监控主机
        '''
        hostip = raw_input('Enter your Host_ip : ')
        groupid = raw_input('Enter you Group_id : ')
        templateid = raw_input('Enter your Template_id : ')
        g_list = []
        t_list = []
        for i in groupid.split(','):
            var = {}
            var['groupid'] = i
            g_list.append(var)
        for i in templateid.split(','):
            var = {}
            var['templateid'] = i
            t_list.append(var)
        if hostip and groupid and templateid:
            data = json.dumps(
                {
                    "jsonrpc":"2.0",
                    "method":"host.create",
                    "params":{
                        "host": hostip,
                        "interfaces":[
                            {
                                "type": 1,
                                "main": 1,
                                "useip": 1,
                                "ip": hostip,
                                "dns": "",
                                "port": "10050"
                            }
                        ],
                        "groups": g_list,
                        "templates": t_list,
                    },
                    "auth": self.authID,
                    "id": 1,
                }
            )
            res =  self.get_data(data,hostip)
            if 'result' in res.keys():
                res = res['result']
                if 'hostids' in res.keys():
                    print "\033[1;32;40m%s\033[0m" % "Create host success"
            else:
                print "\033[1;31;40m%s\033[0m" % "Create host failure: %s" % res['error']['data']
        else:
            print "\033[1;31;40m%s\033[0m" % "Enter Error: ip or groupid or tempateid is NULL,please check it !"

# def main():
#     test = zabbixtools()
#     return test
    # test.host_get()
    # test.template_get()
    # test.hostgroup_get()


# if __name__ == '__main__':
#     host = zabbixtools