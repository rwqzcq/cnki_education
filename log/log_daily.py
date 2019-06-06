import logging
import os
import time

class DailyLog:
    '''
    每天的爬取一直记录
    每天每一个主题 每天一共爬取多少条 更新了多少条
    '''

    def __init__(self):
        '''
        初始化日志的一系列配置
        '''
        self.log_dir = os.path.dirname(__file__) 
        self.log_path = os.path.join(os.path.dirname(__file__), 'daily.log') # 设置日志文件的路径
        logging.basicConfig(filename = self.log_path, level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y-%m-%d') # 配置爬取日志的记录
        self.total = 0 # 总数量为0
        self.updated = 0 # 更新数量为0
    def set_data_format(self):
        '''
        设置日志数据的格式
        '''
        pass

    def add_data(self, total, updated):
        '''
        增加数据
        '''
        self.total += total
        self.updated += updated
    
    def update_data(self, run_time):
        '''
        更新数据
        '''
        formated_data = '''一共爬取:{0} 更新:{1} 程序运行{2}分钟'''.format(self.total, self.updated, run_time)
        logging.info(formated_data)        


    def format_data(self, total, updated, run_time):
        '''
        组织数据

        Args:
         - total 总的数量
         - updated 已经更新的总的数量
         - run_time 程序运行时间
        '''
        formated_data = '''一共爬取:{0} 更新:{1} 程序运行{2}分钟'''.format(total, updated, run_time)
        logging.info(formated_data)
    
    def get_today(self):
        '''
        获取今天爬取的情况
        '''
        pass




