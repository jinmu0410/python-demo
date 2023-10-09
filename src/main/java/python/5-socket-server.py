import socket

## 服务端接受到客户端连接，然后给客户端发送一条消息
socketserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketserver.bind(('127.0.0.1', 9999))

socketserver.listen(5)

while True:
    clientsocket,addr = socketserver.accept()
    print("获取到客户端连接地址 = " + str(addr))

    # 给客户端发送一条消息
    msg = "我已经接收到来自客户端你的消息了"
    clientsocket.send(msg.encode("utf-8"))
    clientsocket.close()