import threading

class MyThread(threading.Thread):
    def __init__(self,thread_name):
        super(MyThread,self).__init__(name=thread_name)

    def run(self):
        print("%s正在运行中......" % self.name)

##main方法
if __name__ == '__main__':
    for i in range(10):
        MyThread("thread-" + str(i)).start()

