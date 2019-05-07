import time
import traceback
import sys
import csv
from paper.paper_parse import get_paper_detail_without_content
from log.log import CnkiLog

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
                    log = dict( current_log, **log)          
    except: 
        traceback.print_exc()
    finally:
        # 写入日志文件
        cnki_log.write_log(log)
        # 写入主文件
        cnki_log.update_csv(full)

if __name__ == "__main__":
    # cnki_main_with_selenium(dataset_path = './init/dataset_2018.csv', log_name = 'log_2018.json', full_name = 'full_2018.csv')
    # 爬取2019年数据
    cnki_main_with_selenium(dataset_path = './init/dataset_2019.csv', log_name = 'log_2019.json', full_name = 'full_2019.csv')
