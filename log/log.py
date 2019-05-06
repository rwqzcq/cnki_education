import os
import csv
import json
import time


class CnkiLog:

    def __init__(self):
        self.log_path = os.path.join(os.path.dirname(__file__), 'log.json')
        self.is_exist = os.path.exists(self.log_path)
        self.csv_path = os.path.join(os.path.dirname(__file__), 'full.csv')

    def get_log(self):
        '''
        获取日志文件
        
        :Returns:
         - Boolean False 不存在日志文件
        '''
        if self.is_exist == False:
            return False
        else:
            with open(self.log_path) as f:
                data = f.read()
                return json.loads(data)

    def check(self, filename):
        '''
        检查当前爬取的论文是否存在于日志中
        改方法不建议使用
        '''
        data = self.get_log()
        if data == False:
            return False # 不存在
        paper_log = data[filename]
        if paper_log['error'] == 1:
            return False # 存在但是出错了
        else:
            return True # 不存在
    
    def write_log(self, data):
        '''
        写入日志文件
        '''
        data = json.dumps(data)
        with open(self.log_path, 'w') as f:
            f.write(data)
    
    def get_full_csv(self):
        '''
        获取csv文件中的内容
        '''
        data = []
        try:
            with open(self.csv_path) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        finally:
            return data
        
    def update_csv(self, new_data):
        '''
        更新csv文件中的内容
        '''
        data = self.get_full_csv()
        # 合并
        data.extend(new_data) # 不用返回
        xuhao = 1
        headers = ["xuhao", "id", 'title', 'author', 'abstract', 'keywords', 'perio', 'juanhao', 'issn', 'read_url', 'pdf_url', 'content', 'original_url']
        with open(self.csv_path, 'w', newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            for row in data:
                # 重新整理index
                row['xuhao'] = xuhao
                writer.writerow(row)
                xuhao += 1