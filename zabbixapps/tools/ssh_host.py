#coding:utf-8
import paramiko

#创建SSH连接函数
def ssh_connect(_host,_username, _password):
    try:
        _ssh_fd = paramiko.SSHClient()
        _ssh_fd.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        _ssh_fd.connect(_host, username=_username, password=_password)
    except Exception, e:
        print ('ssh %s@%s: %s' %(_username, _host, e))
        exit()
    return _ssh_fd

#创建命令执行函数
def ssh_exec_cmd(_ssh_fd, _cmd):
    return _ssh_fd.exec_command(_cmd)

#创建关闭SSH函数
def ssh_close(_ssh_fd):
    _ssh_fd.close()

if __name__ == '__main__':
    sshd = ssh_connect('192.168.100.127', 'root', '123456')
    stdin,stdout,stderr = ssh_exec_cmd(sshd, 'uname -r')
    err_list = stderr.readlines()
    if len(err_list)>0:
        print 'ERROR:' + err_list[0]
        exit()
    for item in stdout.readlines():
        print item
    ssh_close(sshd)