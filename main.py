import time
import traceback
import sys
import csv
from paper.paper_parse import get_paper_detail_without_content


def cnki_main_with_selenium():
    '''
    根据下载的列表来获取论文正文
    '''
    full = []
    log = []
    count = 1
    # 读取csv
    try:
        # 载入日志文件
        with open('./init/dataset_2018.csv', encoding='UTF-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                time.sleep(3)
                filename = row['paper_id']
                # 日志
                row_log = {"filename" : filename, "online" : 0, "not_online" : 0, "error" : 0}
                paper = get_paper_detail_without_content(filename)
                if paper == False:
                    row_log['error'] = 1
                else:
                    paper['xuhao'] = count
                    count = count + 1
                    if paper['read_url'] != False: 
                        row_log['online'] = 1
                    else: # 写入没有在线阅读文件 
                        row_log['not_online'] = 1
                log.append(row_log) 
                full.append(paper)           
    except: 
        traceback.print_exc()
    finally:
        # 写入日志文件
        '''
        filename online not_online error
        '''
        headers = ["filename", "online", "not_online", "error"]
        with open('./log/log.csv', 'w', newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            for row in log:
                writer.writerow(row)
        # 写入主文件
        headers = ["xuhao", "id", 'title', 'author', 'abstract', 'keywords', 'perio', 'juanhao', 'issn', 'read_url', 'pdf_url', 'content', 'original_url']
        with open('./log/full.csv', 'w', newline='', encoding='UTF-8') as f:
            writer = csv.DictWriter(f, headers)
            writer.writeheader()
            for row in full:
                writer.writerow(row)  

if __name__ == "__main__":
    # cnki_main_with_selenium()
    from common.cnki_config import CnkiConfig
    from journal.latest import get_latest_issue, check_if_updated
    '''
    检查是否已经更新
    '''
    config = CnkiConfig()
    journal_id = 'XJJS'
    old = config.get_journal_latest(journal_id)
    r = check_if_updated(journal_id, old)
    
    # journals = config.get_all_journals()
    # latest = {}
    # try:
    #     for journal in journals:
    #         journal_id = journal['cnki_perio_id']
    #         latest[journal_id] = get_latest_issue(journal_id)
    # finally:
    #     config.write_all_latest(latest)