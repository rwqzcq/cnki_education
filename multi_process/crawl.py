import threading
from queue import Queue
from common.journal_config import get_journal_config
from paper.subject_filter import SubjectFilter, SubjectConfig
from paper.paper_parse import get_paper_detail_without_content
from log.log import CnkiLog
from common.journal_config import get_journal_config
from paper.paper_oop import get_paper_obj
from db.journal_db import JournalDb
import time

# https://www.cnblogs.com/derek1184405959/p/8449923.html
class ThreadCrawl(threading.Thread):
    '''
    主题抓取队列
    '''
    def __init__(self, threadName, subect_queue, dataQueue):
        super(ThreadCrawl, self).__init__()
        # 线程名
        self.threadName = threadName
        # 页码队列
        self.subect_queue = subect_queue
        # 数据队列
        self.dataQueue = dataQueue
    
    def run(self):
        print("启动 " + self.threadName)
        while not CRAWL_EXIT:
            try:
                # 取出一个主题，先进先出
                # 可选参数block，默认值为True
                #1. 如果对列为空，block为True的话，不会结束，会进入阻塞状态，直到队列有新的数据
                #2. 如果队列为空，block为False的话，就弹出一个Queue.empty()异常，
                subject = self.subect_queue.get(False)
                # 爬取改主题下的期刊列表
                subject_name = subject['name']
                retreval_str = None
                if subject['retreval_str'] != False:
                    retreval_str = subject['retreval_str']
                start_year = get_journal_config().get('start_year') # 获取起始年
                start_year = str(start_year)
                subject = SubjectFilter(subject_name, start_year = start_year, end_year = '2019', retreval_str = retreval_str) # 校园突发事件
                data = subject.get()
                # 往队列里面放数据
                if data != False:
                    for filename in data:
                        self.dataQueue.put(filename)
                time.sleep(1)
            except:
                pass
        print("结束 " + self.threadName)


class ThreadParse(threading.Thread):
    '''
    论文解析进程
    '''
    def __init__(self, threadName, dataQueue):
        super(ThreadParse, self).__init__()
        # 线程名
        self.threadName = threadName
        # 数据队列
        self.dataQueue = dataQueue

    def run(self):
        db = JournalDb()
        print("启动" + self.threadName)

        while not PARSE_EXIT:
            try:
                filename = self.dataQueue.get(False)
                paper = get_paper_obj(obj_name = 'selenium').get_paper_detail_without_content(filename) # 通过API的方式查询论文的详情
                if paper != false:
                    # 插入数据库
                    db.insert_into_originallink(paper)
            except:
                pass
        print("退出" + self.threadName)
    



CRAWL_EXIT = False
PARSE_EXIT = False