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
            response = json.loads(result.read())
            # pprint(type(response))
            if 'result' in response.keys():
                response = response['result']
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
        # pprint(res)
        # res = res['result']
        return res

    def host_del(self, hostid):
        '''
        通过zabbix API 删除主机
        '''
        # hostip = raw_input('Enter Your Check Host_name: ')
        # pprint(hosts)
        if hostid == 0:
            print "This host cannot find in zabbix,please check it !"
            sys.exit()
        data = json.dumps(
            {
                "jsonrpc":"2.0",
                "method": "host.delete",
                "params":[
                    hostid,
                ],
                "auth":self.authID,
                "id":1
            }
        )
        # pprint(data)
        res = self.get_data(data)
        # pprint(res)
        if 'hostids' in res.keys():
            return "Delet Host:%s success !" % res
        else:
            return "Delet Host:%s failure !" % res

    def host_create(self, hostip, groupid, templateid):
        '''
        通过zabbix API 添加监控主机
        '''
        # hostip = raw_input('Enter your Host_ip : ')
        # groupid = raw_input('Enter you Group_id : ')
        # groupid = '2'
        # templateid = raw_input('Enter your Template_id : ')
        # templateid = '3'
        g_list = []
        t_list = []
        for i in groupid.split(','):
            var = {}
            var['groupid'] = i
            g_list.append(var)
            # pprint(g_list)
        for i in templateid.split(','):
            var = {}
            var['templateid'] = i
            t_list.append(var)
            # pprint(t_list)
        # pprint(hostip)
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
            # pprint(data)
            res = self.get_data(data)
            # pprint(res)
            if 'hostids' in res.keys():
                print "Create host success"
            else:
                print "Create host failure: %s" % res
        else:
            print "Enter Error: ip or groupid or tempateid is NULL,please check it !"
        # pprint(res)
        return json.dumps(res)

# def main():
#     test = Zabbixtools()
#     return test
    # test.host_get()
    # test.template_get()
    # test.hostgroup_get()


# if __name__ == '__main__':
#     host = Zabbixtools