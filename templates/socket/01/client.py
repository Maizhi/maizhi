#encoding=utf-8

import socket
s=socket.socket()
#链接
s.connect(('127.0.0.1', 8000))
#获取键盘输入
msg = raw_input("Please input your message:")
s.sendall(msg)
print s.recv(1024)
s.close()
