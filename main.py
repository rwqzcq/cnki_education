import time
import traceback
import sys
import csv
from paper.paper_parse import get_paper_detail_without_content
from log.log import CnkiLog

def cnki_main_with_selenium():
    '''
    根据下载的列表来获取论文正文
    '''
    cnki_log = CnkiLog()
    current_log = cnki_log.get_log()
    full = []
    log = {}
    count = 1
    # 读取csv
    try:
        # 载入日志文件
        with open('./init/dataset_2018.csv', encoding='UTF-8') as f:
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
        # '''
        # filename online not_online error
        # '''
        # headers = ["filename", "online", "not_online", "error"]
        # with open('./log/log.csv', 'w', newline='', encoding='UTF-8') as f:
        #     writer = csv.DictWriter(f, headers)
        #     writer.writeheader()
        #     for row in log:
        #         writer.writerow(row)
        # 写入主文件
        cnki_log.update_csv(full)

if __name__ == "__main__":
    cnki_main_with_selenium()
    # cnki_log = CnkiLog()
    # full = cnki_log.get_full_csv()
    # print(full)
    # from common.cnki_config import CnkiConfig
    # from journal.latest import get_latest_issue, check_if_updated
    # '''
    # 检查是否已经更新
    # '''
    # config = CnkiConfig()
    # journal_id = 'XJJS'
    # old = config.get_journal_latest(journal_id)
    # r = check_if_updated(journal_id, old)
    
    # journals = config.get_all_journals()
    # latest = {}
    # try:
    #     for journal in journals:
    #         journal_id = journal['cnki_perio_id']
    #         latest[journal_id] = get_latest_issue(journal_id)
    # finally:
    #     config.write_all_latest(latest)