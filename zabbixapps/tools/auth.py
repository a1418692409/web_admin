#!/usr/bin/env python
#conding=utf-8

import json
import urllib2

def get_authid():
    # url = "http://zabbix.yitong111.com/zabbix/api_jsonrpc.php"
    url = "http://192.168.1.43/zabbix/api_jsonrpc.php"
    header = {"Content-Type":"application/json"}
    data = json.dumps(
    {
        "jsonrpc":"2.0",
        "method":"user.login",
        "params":{
            # "user":"admin",
            # "password":"yitong988"
            "user":"zabbix",
            "password":"zabbix",
        },
        "id":0
    }
    )
    request = urllib2.Request(url,data)
    for key in header:
        request.add_header(key,header[key])
    try:
        result = urllib2.urlopen(request)

    except Exception as e:
        print "Auth Failed, Please Check Your Name And Password:",e.code
    else:
        response = json.loads(result.read())
        return response
        result.close()
        # print "Auth Successful. The Auth ID Is:",response['result']