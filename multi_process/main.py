from multi_process.subject_queue import get_subject_queue
from multi_process.crawl import ThreadCrawl, ThreadParse
from queue import Queue

def work_use_muli_process():
    '''
    多线程爬虫
    '''
    # 三个采集线程的名字
    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]
    # 存储三个采集线程的列表集合
    threadcrawl = []
    pageQueue = get_subject_queue()
    dataQueue = Queue()

    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)

    # 三个解析线程的名字
    parseList = ["解析线程1号","解析线程2号","解析线程3号"]
    # 存储三个解析线程
    threadparse = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue)
        thread.start()
        threadparse.append(thread)

    # 等待pageQueue队列为空，也就是等待之前的操作执行完毕
    while not pageQueue.empty():
        pass

    # 如果pageQueue为空，采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True

    print("pageQueue为空")

    for thread in threadcrawl:
        thread.join()
        print("1")

    while not dataQueue.empty():
        pass

    global PARSE_EXIT
    PARSE_EXIT = True

    for thread in threadparse:
        thread.join()
        print("2")