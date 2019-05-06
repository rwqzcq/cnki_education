import os
import json

class CnkiConfig:
    '''
    从配置文件中获取程序的配置信息，比如期刊列表等
    '''
    def __init__(self):
        self.journal_list_path = os.path.join(os.path.dirname(__file__), '教育CSSCI期刊_CNKI.json')
        self.journal_latest_path = os.path.join(os.path.dirname(__file__), '教育CSSCI期刊_最新周期.json')

    def get_all_journals(self):
        '''
        获取所有期刊
        '''
        with open(self.journal_list_path) as f:
            data = f.read()
        data = json.loads(data)
        return data["list"]
    
    def write_all_latest(self, data):
        '''
        写入最新周期文件

        '''
        data = json.dumps(data)
        with open(self.journal_latest_path, 'w') as f:
            f.write(data)

    def get_all_latest(self):
        '''
        获取所有最新出版周期
        '''
        with open(self.journal_latest_path) as f:
            data = f.read()
        data = json.loads(data)
        return data

    def update_latest(self, data):
        '''
        更新最新的出版周期并写入文件

        :Args:
         - data: 字典
        '''
        old = self.get_all_latest()
        for zhouqi in data:
            journal_id = zhouqi['journal_id']
            old[journal_id] = zhouqi
        self.write_all_latest(old) # 写文件
    
    def check_latest_if_updated(self, journal_id):
        '''
        检查某一期刊是否有更新
        '''
        pass
    
    def get_journal_latest(self, journal_id):
        '''
        获取某一期刊的最新的出版周期
        '''
        return self.get_all_latest()[journal_id]
        
        
    
    
    
    

