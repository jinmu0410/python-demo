import threading
import time

def test(arg):
    time.sleep(1)
    print("thread-" + str(arg) + " running.....")

if __name__ == '__main__':
    for i in range(10):
        threading.Thread(target=test(i)).start()