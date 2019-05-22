from socket import *
import os,sys

#服务器地址
ADDR = ('127.0.0.1',9911)

#发送消息
def send_msg(s,name):
    while True:
        try:
            text=input("发言：")
        except KeyboardInterrupt:
            text="quit"
        if text=="quit":
            msg="Q "+name
            s.sendto(msg.encode(),ADDR)
            sys.exit("退出聊天")
        msg="C %s %s"%(name,text)
        s.sendto(msg.encode(),ADDR)


#接收消息
def recv_msg(s):
    while True:
        data,addr=s.recvfrom(1024)
        if data.decode()=='EXIT':
            sys.exit()
        print(data.decode())

#创建网络链接
def main():
    s=socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    #s.bind(('0.0.0.0',9911)) #可设置可不设置
    while True:
        name=input('姓名：')
        msg="L " + name
        #等待回应
        s.sendto(msg.encode(),ADDR)
        data,addr=s.recvfrom(1024)
        if data.decode()=="ok":
            print('您已进入聊天室')
            break
        else:
            print(data.decode())
    #创建新的进程
    pid=os.fork()
    if pid<0:
        sys.exit("Error")
        print('user[%s]=%s'%(name,user[name]))
    elif pid==0:

        send_msg(s,name)
    else:
        recv_msg(s)

if __name__ == "__main__":
    main()