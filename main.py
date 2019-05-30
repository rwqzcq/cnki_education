import time
import traceback
import sys
import csv
from paper.paper_parse import get_paper_detail_without_content
from log.log import CnkiLog
from paper.subject_filter import SubjectFilter, SubjectConfig
from common.journal_config import get_journal_config
from paper.paper_oop import get_paper_obj
from db.journal_db import JournalDb
# 多线程模块
from multi_process.subject_queue import get_subject_queue
from multi_process.crawl import ThreadCrawl, ThreadParse
from queue import Queue
# 新日志模块
from log.year_log import CnkiYearLog

# 解析模块
from common.parse import parse_from_filename

# 日志转化模块

from log.year_log import all_into_one_year


def cnki_main_with_selenium(dataset_path, log_name, full_name):
    '''
    根据下载的论文列表来获取论文的详细信息
    
    :Args:
     - dataset_path: csv文件路径
     - log_name: 日志文件名
     - full_name: 最终存储的csv文件名
    '''
    cnki_log = CnkiLog(log_name, full_name)
    current_log = cnki_log.get_log()
    full = []
    log = {}
    count = 1
    # 读取csv
    try:
        # 载入日志文件
        with open(dataset_path, encoding='UTF-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                filename = row['paper_id']
                # 检查日志
                if current_log != False:
                    if filename in current_log:
                        if current_log[filename]['error'] == 0:
                            print(filename + "--已经爬取")
                            continue
                time.sleep(3)
                # 日志
                row_log = {"filename" : filename, "online" : 0, "not_online" : 0, "error" : 0}
                paper = get_paper_detail_without_content(filename)
                if paper == False:
                    row_log['error'] = 1
                else:
                    paper['xuhao'] = count
                    full.append(paper) 
                    count = count + 1
                    if paper['read_url'] != False: 
                        row_log['online'] = 1
                    else: # 写入没有在线阅读文件 
                        row_log['not_online'] = 1
                log[filename] = row_log
                if current_log != False: # 合并日志
                    log = dict(current_log, **log)          
    except: 
        traceback.print_exc()
    finally:
        # 写入日志文件
        cnki_log.write_log(log)
        # 写入主文件
        cnki_log.update_csv(full)

def cnki_get_paper_detail_throgh_list(data_list, file_name):
    '''
    通过filename的id列表来采集论文的相关核心信息

    :Args:
     - data_list: 存放filename的列表
     - file_name: 存放的csv文件名和文件日志名
    '''
    cnki_log = CnkiLog(file_name, file_name)
    current_log = cnki_log.get_log()
    full = []
    log = {}
    count = 1
    try:
        for filename in data_list:
            if current_log != False:
                if filename in current_log:
                    if current_log[filename]['error'] == 0:
                        print(filename + "--已经爬取")
                        continue
            # 日志
            row_log = {"filename" : filename, "online" : 0, "not_online" : 0, "error" : 0}
            # paper = get_paper_detail_without_content(filename)
            paper = get_paper_obj(obj_name = 'api').get_paper_detail_without_content(filename) # 通过API的方式查询论文的详情
            if paper == False:
                row_log['error'] = 1
            else:
                paper['xuhao'] = count
                paper['subject'] = file_name # 增加主题
                full.append(paper) 
                count = count + 1
                if paper['read_url'] != False: 
                    row_log['online'] = 1
                else: # 写入没有在线阅读文件 
                    row_log['not_online'] = 1
            log[filename] = row_log
            if current_log != False: # 合并日志
                log = dict(current_log, **log)    
    except:
        traceback.print_exc()
    finally:
        # 写入日志文件
        if log != {}:
            cnki_log.write_log(log)
        # 写入数据库与所对应的csv文件
        if len(full) > 0:
            cnki_log.use_db().insert_into_originallink_multi(full)
            # cnki_log.update_csv(full)



def cnki_subject_with_selenium(subject):
    '''
    爬取某一主题下的C刊教育类论文

    :Args:
     - subject: 主题对象 包括主题名称以及该主题所包括的关键词

    '''
    subject_name = subject['name']
    retreval_str = None
    if subject['retreval_str'] != False:
        retreval_str = subject['retreval_str']
    start_year = get_journal_config().get('start_year') # 获取起始年
    start_year = str(start_year)
    subject = SubjectFilter(subject_name, start_year = start_year, end_year = '2019', retreval_str = retreval_str) # 校园突发事件
    data = subject.get()
    # 将这个data先存入列表？
    if data != False:
        if len(data) > 0: # 有数据
            cnki_get_paper_detail_throgh_list(data, subject_name)


def insert_csv_into_db():
    '''
    将csv文件里面的数据放到数据库中

    '''
    subject_config = SubjectConfig()
    subject_list = subject_config.get_subjects()
    for subject in subject_list:   
        subject_name = subject['name']
        if subject_name != '学生会治理': # 先过滤掉校园突发事件
            continue
        cnki_log = CnkiLog(subject_name, subject_name)
        current_log = cnki_log.get_log() # 读取日志文件
        full = cnki_log.get_full_csv() # 获取所有csv文件中的内容
        log = {}
        for paper in full:
            filename = paper['id']
            if current_log != False:
                if filename in current_log:
                    if current_log[filename]['error'] == 0:
                        print(filename + "--已经爬取并存储")
                        continue
            paper['subject'] = subject_name
            try:
                r = cnki_log.use_db().insert_into_originallink(paper) # 插入数据一条一条插入
                row_log = {"filename" : filename, "online" : 1, "not_online" : 0, "error" : 0}
                if r == False:
                    row_log['error'] = 1
                else:
                    print(filename + "--插入成功")
                    row_log['error'] = 0
            finally:
                # 更新日志
                log[filename] = row_log
                if current_log != False:
                    log = dict(current_log, **log)
                if log != {}:
                    cnki_log.write_log(log)



def work():
    '''
    入口程序
    '''
    subject_config = SubjectConfig()
    subject_list = subject_config.get_subjects()
    for subject in subject_list:
        cnki_subject_with_selenium(subject)

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



if __name__ == "__main__":
    # 开启个定时任务
    # work()
    # work_use_muli_process()
    # new_log = CnkiYearLog(log_name = 'test', year = '2018')
    # log = new_log.get_log()
    # print(log)

    # 日志数据转换
    subject_config = SubjectConfig()
    subject_list = subject_config.get_subjects()
    for subject in subject_list:
        all_into_one_year(subject_name = subject['name'])
    # /日志数据转换
    # 测试数据库查询
    # db = JournalDb()
    # result = db.get_all_filename_of_one_subject(subject_name = '教师队伍建设')
    # print(result)
    # /测试数据库查询

    # 测试解析函数
    # info = parse_from_filename(filename = 'SIXI2015S6005')
    # print(info)
    # /测试解析函数

    # 测试日志数据转换
    # all_into_one_year(subject_name = '校园突发事件')
    # /测试日志数据转换