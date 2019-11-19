"""
httpserver v2.0
io多路复用 和 http协议训练

接收客户端（浏览器）请求
解析客户端发送的请求
根据请求组织数据内容
将数据内容形成http响应格式返回给浏览器
"""
from socket import *
from select import *


# 具体的功能实现
class HTTPServer:
    def __init__(self, host='0.0.0.0', port=8000, dir=None):
        self.host = host
        self.port = port
        self.address = (host, port)
        self.dir = dir
        self.create_socket()  # 创建套接字
        self.rlist = []
        self.wlist = []
        self.xlist = []

    def create_socket(self):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(self.address)

    # 启动服务
    def serve_forever(self):
        self.sockfd.listen(3)
        print("Listen the port %d" % self.port)
        # IO多路复用循环监听客户端请求
        self.rlist.append(self.sockfd)  # 将套接字监控
        while True:
            rs, ws, xs = select(self.rlist,
                                self.wlist,
                                self.xlist)
            # 遍历返回值列表,根据情况讨论
            for r in rs:
                # 有客户端链接(浏览器)
                if r is self.sockfd:
                    c, addr = r.accept()
                    self.rlist.append(c)  # 将c添加到读关注
                else:
                    self.handle(r)  # 浏览器给我发http请求

    # 处理具体的客户端请求
    def handle(self, connfd):
        # 获取http请求
        data = connfd.recv(1024 * 4).decode()
        if not data:
            return
        # 简单的解析
        request_line = data.split('\n')[0]
        info = request_line.split(' ')[1]  # 提取请求内容
        print("请求内容:", info)
        # 将请求内容分为两类 (网页,其他)
        if info == '/' or info[-5:] == '.html':
            self.get_html(connfd, info)
        else:
            self.get_data(connfd, info)

    # 处理网页
    def get_html(self, connfd, info):
        if info == '/':
            filename = self.dir + "/index.html"
        else:
            filename = self.dir + info
        try:
            fd = open(filename)
        except:
            # 网页不存在
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += '\r\n'
            response += "Sorry...."
        else:
            # 网页存在
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += '\r\n'
            response += fd.read()
        finally:
            # 将结果发送给浏览器
            connfd.send(response.encode())

    # 处理其他
    def get_data(self, connfd, info):
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += '\r\n'
        response += "<h1>Waiting for httpserver 3.0</h1>"
        connfd.send(response.encode())


if __name__ == '__main__':
    """
    通过HTTPServer类可以快速的搭建一个服务,帮助我展示我的网页
    使用原则 : 1. 能够为使用者实现的尽量都实现
              2. 不能替用户决定的数据量让用户传入类中
              3. 不能替用户决定的功能让用户去重写
    """
    # 用户自己设定参数
    host = '0.0.0.0'
    port = 8000
    dir = "./static"  # 网页位置

    httpd = HTTPServer(host, port, dir)  # 实例化对象
    httpd.serve_forever()  # 启动服务
