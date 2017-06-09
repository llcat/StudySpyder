"""
    尝试下多进程编程的api,不是很熟
"""
# python对进程的抽象
from multiprocessing import Process, Pool, Pipe, Queue, Lock, Manager
import os
import time
import random
# python由于全局GIL的原因,多线程不能真正提高性能
# 所以我们采用多进程绕过GIL机制
# 可以看看linux下的进程树(pstree)
# systemd─┬─ModemManager─┬─{gdbus}
#         │              └─{gmain}
#         ├─NetworkManager─┬─dhclient
#         │                ├─dnsmasq
#         │                ├─{gdbus}
#         │                └─{gmain}
#         ├─accounts-daemon─┬─{gdbus}
#                           └─{gmain}
# 所有的子进程都是从初始的systemed进程中fork出来的,组成了一颗进程树,在创建子进程时,
# 使用系统提供的fork()函数


def get_pid(info):
    print(info)
    print("pid:", os.getpid())
    print("parent id:", os.getppid())


def work(info):
    get_pid(info)


def cal_multiply(x):
    return x*x


def pipe_head(conn_head1, conn_head2):
    conn_head1.send([1, 2, 3, 4, 5])
    conn_head2.send([6, 7, 8, 9, 10])
    while True:
        flag1 = conn_head1.recv()
        print("flag1:", flag1)
        if flag1 == 0:
            conn_head1.send([1, 2, 3, 4, 5])
        flag2 = conn_head2.recv()
        print("flag2:", flag2)
        if flag2 == 1:
            conn_head2.send([6, 7, 8, 9, 10])


def pipe_end(conn_end, wait=0, flag=0):
    count = []
    while True:
        tasks = conn_end.recv()
        count.append(tasks)
        print("count -", flag, ": ", len(count))
        l = len(tasks)
        for i in range(l):
            print(tasks.pop())
            time.sleep(wait)
        conn_end.send(flag)


def task_producer(d_ques, count, tasks):
    def generate_list():
        return [random.randint(1, 10)]*5

    for d_qu in d_ques:
        d_qu['recv_q'].put(generate_list())
    while True:
        for d_qu in d_ques:
            try:
                flag = d_qu['send_q'].get(block=False)
                if flag is True:
                    d_qu['recv_q'].put(generate_list())
                    count.value += 1
                    print("tasks:",tasks)
            except Exception as e:
                continue


def task_consumer(d_que, lock, resu, wait=0):
    while True:
        recv = d_que['recv_q'].get()
        print(os.getpid(), ": ", recv)
        lock.acquire()
        try:
            resu.append(recv)
        finally:
            lock.release()
        time.sleep(wait)
        d_que['send_q'].put(True)


def test_return():
    return 1, {'aa': 2}

if __name__ == "__main__":
    rt = test_return()
    print(rt)
    # 查看下进程的id,就知道子进程是否是从父进程中fork出来的呢
    get_pid("main")
    process1 = Process(target=work, args=("child",))
    process1.start()
    # 一个使用线程进行并行计算的例子
    with Pool(5) as p:
        result = p.map(cal_multiply, [1, 2, 3])
    print(result)  # [1, 4, 9]
    # 两个进程间使用Pipe进行信息的交换
    conn1, conn2 = Pipe()
    conn1_1, conn2_1 = Pipe()
    process_head = Process(target=pipe_head, args=(conn1, conn1_1,))
    process_end = Process(target=pipe_end, args=(conn2,))
    process_end1 = Process(target=pipe_end, args=(conn2_1, 3, 1,))
    # process_head.start()
    # process_end.start()
    # process_end1.start()
    # 通过上面的例子,我们可以看到,Pipe的通信方式是阻塞的,也就是说
    # 在我即将完成的dispatcher中是不可行的,我有3个消费者(downloader),一个生产者(url_manager)
    # 当消费者消耗完资源,向生产者请求新的url时,必须等待生产者监听的其他消费者也给他发送请求信息.
    # 所以我们用Queue来传递消息
    r = Manager().list()
    count = Manager().Value("count", 0)
    tks = 10
    print(type(r))
    d_queues = [{"send_q": Queue(4), "recv_q": Queue(4)}]*3
    producer = Process(target=task_producer, args=(d_queues, count, tks))
    producer.start()
    wait = 5
    print(len(d_queues))
    l = Lock()
    for d_q in d_queues:
        Process(target=task_consumer, args=(d_q, l, r, wait)).start()
        # wait += 2

    # 上面的例子我们用Queue实现了一个生产者多个消费者的例子
    # 其中生产者轮询是否有消费者完成了工作,不阻塞等待,如果没有就pass,如果有,就向消费者传递产品.
    # 现在,我们需要解决的在消费者中使用同一个变量的问题,将下载的内容存到同一个list中,应该引入锁机制
    # 如果实现成功,那么我们就可以将这个框架用到我们的dispatcher中,
    # 多进程间共享变量只能使用
    while True:
        if len(r) > 0:
            print("before:", len(r))
            time.sleep(20)
            print("in main print", r.pop())
            print("after:", len(r))
            print("count generate", count.value)
        else:
            pass
