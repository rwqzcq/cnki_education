from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

def get_latest_issue(journal_id):
    '''
    找到某一期刊最新的出版记录 精确到哪一年哪一期

    :Args:
     - journal_id: 期刊ID

    :Returns:
     - Dcit: 成功则返回一个字典
     - Boolean: 失败则返回False

    '''
    latest = {}
    try:
        browser = webdriver.Chrome()
        # step_1 打开网页
        journal = '''http://navi.cnki.net/KNavi/JournalDetail?pcode=CJFD&pykm={0}'''.format(journal_id)
        browser.get(journal)
        browser.implicitly_wait(10)
        latest['journal_id'] = journal_id
        try: # 找到年
            year = browser.find_element_by_css_selector('div.yearissuepage dl dt em')
            latest['year'] = year.text 
            try: # 找到期数
                a = browser.find_element_by_css_selector('div.yearissuepage dl dd a')
                latest['issue'] = a.get_attribute("text")
            except NoSuchElementException as msg:
                return False
        except NoSuchElementException as msg:
            return False
    except NoSuchElementException as msg:
        return False
    finally:
        browser.quit()
    return latest

def check_if_updated(journal_id, old):
    '''
    检查某一个期刊是否已经更新

    :Args:
     - journal_id 期刊ID
     - old 原有的字典
    
    :Returns:
     - Boolean False 不需要更新
     - Dict latest 返回最新的期刊
    '''
    latest = get_latest_issue(journal_id)
    if latest == False: # 没有最新的
        return False
    if (latest['journal_id'] == old['journal_id']) and (latest['year'] == old['year']) and(latest['issue'] == old['issue']): # 两者相同
        return False
    else: # 有最新的
        return latest



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
# '''
# JFJJ => JYYJ
# GXSJ => SLLJ
# BJPL => JYPL
# '''

# if __name__ == "__main__":
#     journal_id = 'JYPL'
#     latest = get_latest_issue(journal_id)
#     print(latest)