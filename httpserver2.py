"""
httpsever 2.0
>io 并发处理
>基本的reques请求
>使用类封装
"""
from socket import *
from select import select


#将具体 HTTP server 功能封装
class HTTPServer:
    def __init__(self,server_address,static_dir):
        self.server_address=server_address
        self.static_dir=static_dir
        self.rlist = []
        self.wlist = []
        self.xlist = []
        self.create_socket()
        self.bind()
    def create_socket(self):
        self.sockfd=socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    def bind(self):
        self.sockfd.bind(self.server_address)
        self.ip=self.server_address[0]
        self.port=self.server_address[1]
    def serve_forever(self):
        self.sockfd.listen(5)
        print("Listen the port %d"%self.port)
        self.rlist.append(self.sockfd)
        while True:
            rs,ws,xs=select(self.rlist,self.wlist,self.xlist)
            for r in rs:
                if r is self.sockfd:
                    c,addr=r.accept()
                    print('Connect from:',addr)
                    self.rlist.append(c)
                else:
                    #处理浏览器请求
                    self.handle(r)
    #处理客户端请求
    def handle(self,connfd):
        #接受下HTTP请求
        request=connfd.recv(4096)
        #防止浏览器断开
        if not request:
            self.rlist.remove(connfd)
            connfd.close()
            return
        #请求解析
        request_line=request.splitlines()[0]
        info=request_line.decode().split(' ')[1]
        print(connfd.getpeername(),':',info)

        #info 分为网页和其他
        if info=='/' or info[-5:] =='.html':
            self.get_html(connfd,info)
        else:
            self.get_data(connfd,info)

        self.rlist.remove(connfd)
        connfd.close()
    #处理网页
    def get_html(self,connfd,info):
        if info=='/':

            filename = self.static_dir + '/index.html' # 网页文件
        else:

            filename=self.static_dir+info
        try:
            fd=open(filename)
        except Exception:
            #没有网页
            responseHeaders="HTTP/1.1 404 Not Found\r\n"
            responseHeaders+='\r\n'
            responseBody="<h1>Sorry Not Found the page</h1>"
        else:
            responseHeaders = "HTTP/1.1 200 OK\r\n"
            responseHeaders += '\r\n'
            responseBody = fd.read()
        finally:
            response=responseHeaders+responseBody
            connfd.send(response.encode())
        #其他情况
    def get_data(self,connfd,info):
        responseHeaders = "HTTP/1.1 200 OK\r\n"
        responseHeaders += '\r\n'
        responseBody = "<h1>Waitting for httpserver 3.0</h1>"
        response = responseHeaders + responseBody
        connfd.send(response.encode())

#如何使用HTTPserver类
if __name__=="__main__":
    #用户自己决定：网页，内容
    server_addr=("0.0.0.0",8000)
    static_dir="./static"  #网页存放地址

    http=HTTPServer(server_addr,static_dir)#生成实例对象
    http.serve_forever()#启动服务

