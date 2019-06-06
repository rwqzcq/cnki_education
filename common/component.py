from selenium import webdriver
# from paper.subject_filter import SubjectFilter, SubjectConfig
from log.log import CnkiLog
from common.journal_config import get_journal_config
from selenium.webdriver.remote.remote_connection import LOGGER
import logging


'''
全局组件文件
应对不同将代码放到不同的环境的时候由于参数的设置所出现的偏差
比如webdriver中的配置选项
'''


def get_webdriver():
    '''
    获取webdriver
    '''
    LOGGER.setLevel(logging.INFO)  # 关闭日志
    path = get_journal_config().get('chrome_webdriver_path')
    if path == False:
        browser = webdriver.Chrome()
    else:
        browser = webdriver.Chrome(path)
    return browser

# def insert_csv_into_db():
#     '''
#     将csv文件里面的数据放到数据库中
#     '''
#     subject_config = SubjectConfig()
#     subject_list = subject_config.get_subjects()
#     for subject in subject_list:
#         subject_name = subject['name']
#         if subject_name != '学生会治理': # 先过滤掉校园突发事件
#             continue
#         cnki_log = CnkiLog(subject_name, subject_name)
#         current_log = cnki_log.get_log() # 读取日志文件
#         full = cnki_log.get_full_csv() # 获取所有csv文件中的内容
#         log = {}
#         for paper in full:
#             filename = paper['id']
#             if current_log != False:
#                 if filename in current_log:
#                     if current_log[filename]['error'] == 0:
#                         print(filename + "--已经爬取并存储")
#                         continue
#             paper['subject'] = subject_name
#             try:
#                 r = cnki_log.use_db().insert_into_originallink(paper) # 插入数据一条一条插入
#                 row_log = {"filename" : filename, "online" : 1, "not_online" : 0, "error" : 0}
#                 if r == False:
#                     row_log['error'] = 1
#                 else:
#                     print(filename + "--插入成功")
#                     row_log['error'] = 0
#             finally:
#                 # 更新日志
#                 log[filename] = row_log
#                 if current_log != False:
#                     log = dict(current_log, **log)
#                 if log != {}:
#                     cnki_log.write_log(log)
