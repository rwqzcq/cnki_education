import os
import json
from log.log import CnkiLog

class CnkiYearLog(CnkiLog):
    '''
    结合时间的日志管理
    '''
    def __init__(self, log_name, year):
        '''
        :Args:
         - log_name: 日志文件名字
         - year: 时间
        '''
        self.log_path = os.path.join(os.path.abspath('./log/' + year), log_name + '.json')
        self.is_exist = os.path.exists(self.log_path)
        self.log_dir = os.path.abspath('./log/' + year) # 创建文件夹 要不然写不进去数据
        if not os.path.exists(self.log_dir):
            os.mkdir(self.log_dir)
    


