#encoding=utf-8

import socket
s=socket.socket()
#建立socket链接
s.bind(('127.0.0.1',8000))
#监听连接请求，其中的1 ，是指监听一个
s.listen(1)
#进行循环，一直监听client发来的消息
while 1:
#获取链接IP和端口
    conn,addr=s.accept()
    print '['+addr[0]+':'+str(addr[1])+'] send a message to me: '+conn.recv(1024)
    conn.sendall('I received a message from ['+addr[0]+':'+str(addr[1])+']')
s.close()
