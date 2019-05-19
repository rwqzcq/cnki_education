from common.journal_config import get_journal_config
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

'''
解析CNKI中某一篇论文的详细信息
'''
class CnkiJournalDetailWithStr:
    '''解析CNKI期刊详情页
    如果解析某一个字段为空则全部返回空字符串
    '''
    def __init__(self, soup):
        self.soup = soup

    # 获取标题
    def get_title(self):
        title = self.soup.select_one('h2.title')
        return title.get_text()
    # 获取作者
    def get_author(self):
        try:
            authors = self.soup.select('div.author a')
            author = ''
            for node in authors:
                author = author + node.get_text() + " "
            # 去除最后一个空格
            author = author.rstrip()
            return author
        except:
            return ''
    # 获取摘要
    def get_abstract(self):
        abstract = self.soup.select_one('#ChDivSummary')
        if abstract:
            return abstract.get_text()
        else:
            return ''
    # 关键词
    def get_keywords(self):
        try:
            keywords = self.soup.select('#catalog_KEYWORD ~ a')
            keyword = ''
            for node in keywords:
                original_keyword = node.get_text()
                filter = original_keyword.replace('\n', '').replace(' ', '').replace('\r', '') # 关键词过滤空格
                keyword  = keyword + filter + " "
            keyword = keyword.rstrip()
            return keyword
        except:
            return ''
    # 获取期刊
    def get_perio(self):
        perio = self.soup.select_one('p.title')
        return perio.get_text()
    # 获取ISSN
    def get_issn(self):
        try:
            issn = self.soup.select('div.sourinfo p')[3]
            issn = issn.get_text()
            issn = issn.replace('ISSN：', '').replace('\r', '').replace('\n', '').replace(' ', '')
            return issn
        except:
            return ''
    # 获取卷期-出版日期
    def get_publish_date(self):
        try:
            date = self.soup.select('div.sourinfo p')[2]
            a = date.select_one('a').get_text()
            a = a.replace('\r', '').replace('\n', '').replace(' ', '') # 去除换行符 空格
            a = a.replace('期', '') # 去除期字
            return a
        except:
            return ''

    # 获取下载PDF的链接
    def get_download_url(self):
        try:
            pdf_download_url = self.soup.select_one('#pdfDown')
            download_url = get_journal_config().get('cnki_base_url') + pdf_download_url['href']
            return download_url              
        except:
            return ''

    # 获取在线阅读的链接
    def get_online_reading_url(self):
        try:
            online_read = self.soup.select_one('.icon.icon-dlcrsp.xml')
            url = online_read['href']
            url = get_journal_config().get('cnki_base_url') + url
            return url          
        except:
            return ''

# 从详情页中解析所需要的数据 单纯的数据 不包括 原文
def get_pure_detail_from_detail_page(soup, filename):
    '''
    从详情页中解析所需要的数据，不包括原文

    :param soup: beautifulsoup实例
    :param filename: cnki中某一篇论文的唯一标识符
    '''
    # 如果文献不存在
    none = soup.select_one('div.sorry p')
    if none:
        print("文献不存在")
        return False
    paper = {}
    # detail = CnkiJournalDetail(soup)
    detail = CnkiJournalDetailWithStr(soup)
    # 解析ID
    paper['id'] = filename
    # 解析标题
    paper['title'] = detail.get_title()
    # 解析作者
    paper['author'] = detail.get_author()
    # 解析摘要
    paper['abstract'] = detail.get_abstract()
    # 解析关键词
    paper['keywords'] = detail.get_keywords()
    # 解析期刊
    paper['perio'] = detail.get_perio()
    # 解析卷号
    paper['juanhao'] = detail.get_publish_date()
    # 解析ISSN
    paper['issn'] = detail.get_issn()
    read_url = detail.get_online_reading_url()
    paper['read_url'] = read_url
    paper['pdf_url'] = detail.get_download_url()
    paper['content'] = ''
    # 获取详情链接
    source_url = '''http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename={0}'''.format(filename)
    paper['original_url'] = source_url
    return paper

# 使用selenium爬取期刊不包括正文的部分
def get_paper_detail_without_content(filename):
    '''
    使用selenium爬取期刊不包括正文的部分

    :param filename: cnki中某一篇论文的唯一标识符
    '''
    source_url = '''http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename={0}'''.format(filename)
    browser = webdriver.Chrome() # mac程序中没有出现
    try:
        browser.implicitly_wait(10) # 设置隐式的等待时间 全局的
        browser.get(source_url) # 打开网页
        # 获取网页源代码
        html = browser.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, 'html.parser')
        paper = get_pure_detail_from_detail_page(soup, filename)
        if paper == False:
            print(filename + "--文献不存在")
            return False
        return paper
    except:
        # 写入错误文件
        print("错误了")
        return False
    finally:
        browser.quit() # 这里不用返回信息

