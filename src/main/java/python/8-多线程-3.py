import time
from concurrent.futures import ThreadPoolExecutor

#线程池

def work(n):
    print(f"开始执行任务{n}")
    time.sleep(2)
    print(f"任务{n}执行完毕")
    return n * 2

def main():
    with ThreadPoolExecutor(4) as executor:
        results = executor.map(work, range(1,6))
    for result in results:
        print(f"任务结果：{result}")


if __name__ == '__main__':
    main()