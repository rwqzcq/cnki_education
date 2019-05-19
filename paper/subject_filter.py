from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.parse import parse_filename
from common.journal_config import get_journal_config
import time
import traceback

class SubjectFilter:
    '''
    爬取某一主题下的论文
    '''
    def __init__(self, subject, start_year, end_year, retreval_str):
        '''
        构造方法
        
        :Args:
         - subject: 主题词
         - start_year: 开始年份
         - end_year: 结束年份
         - retreval_str: 检索式
        '''
        self.subject = subject
        self.start_year = start_year
        self.end_year = end_year
        if retreval_str == None: # 自己有检索式就用自己的检索式
            self.build_retreval()
        else:
            self.retreval_str = retreval_str
        
    
    def build_retreval(self):
        '''
        创建检索式
        从配置项中读取关键词构成检索式
        '''
        self.retreval_str = ''' SU = '{0}' '''.format(self.subject)
    
    def get(self):
        '''
        爬取数据
        '''
        browser = webdriver.Chrome()
        url = 'http://kns.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ'
        browser.implicitly_wait(10)
        browser.get(url)
        try:
            search = browser.find_element_by_xpath('//*[@id="1_2"]/a')
            browser.execute_script("arguments[0].click();", search) # 点击切换到专业检索
            try:
                input_id = 'expertvalue'
                input = WebDriverWait(browser, 10).until(           
                                    EC.presence_of_element_located((By.ID, input_id)))
                input.send_keys(self.retreval_str) # 输入检索式
                try:
                    select_id = 'year_from'
                    select_from = browser.find_element_by_id(select_id) # 找到起始的年限
                    Select(select_from).select_by_value(self.start_year) # 选择起始年限
                    try:
                        select_id = 'year_to'
                        select_end = browser.find_element_by_id(select_id) # 找到终止年限
                        Select(select_end).select_by_value(self.end_year) # 选择终止年限
                        try:
                            cssci_id = 'mediaBox4'
                            cssci_checkbox = browser.find_element_by_id(cssci_id) # 找到cssci期刊选项
                            browser.execute_script("arguments[0].click();", cssci_checkbox) # 点击该选项
                            try:
                                search_id = 'btnSearch'
                                search = browser.find_element_by_id(search_id) # 找到检索按钮
                                browser.execute_script("arguments[0].click();", search) # 点击该选项
                                # 显示等待元素加载完毕
                                try:
                                    content_frame_id = 'iframeResult'
                                    content_iframe = WebDriverWait(browser, 10).until(           
                                        EC.presence_of_element_located((By.ID, "iframeResult")))
                                    browser.switch_to.frame(content_frame_id) # 切换到iframe
                                    try:
                                        data = []
                                        # 为了减少等待时间 就在这个地方先进行一个爬取 然后再去递归操作
                                        data = self.fanye(browser, data)
                                        return data
                                    except:
                                        print("切换iframe出问题")
                                        return False
                                except:
                                    return False
                                # try:
                                #     time.sleep(3)
                                #     content_frame_id = 'iframeResult'
                                #     browser.switch_to.frame(content_frame_id) # 切换到iframe
                                #     try:
                                #         journal_lists = browser.find_elements_by_css_selector("a.fz14")
                                #         print(len(journal_lists))
                                #         print("找到了")
                                #     except:
                                #         print("没有找到论文列表")                              
                                # except:
                                #     print("切换失败了")
                                #     pass
                            except:
                                print("找不到检索项")
                                return False
                        except:
                            print("找不到cssci选项")
                            return False
                    except:
                        print("找不到终止年")
                        return False
                except:
                    print("找不到起始年")
                    return False
            except:
                print("找不到输入框")
                return False
        except:
            print("找不到检索标识")
            return False
        finally:
            browser.close()

    def fanye(self, browser, data):
        '''
        执行翻页操作
        :Args:
         - browser 浏览器对象
         - data 要返回的数据
        '''

        try:
            # 显示等待元素加载完成
            journal_lists = WebDriverWait(browser, 10).until(           
                                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.fz14")))
            # journal_lists = browser.find_elements_by_css_selector("a.fz14")                     
            if journal_lists: # 有期刊
                for journal in journal_lists:
                    href = journal.get_attribute("href")
                    filename = parse_filename(href)
                    data.append(filename)
                try:
                    page_next = browser.find_element_by_css_selector(".TitleLeftCell a:last-child ") # 找到翻页的标志
                    if page_next.text == '下一页':
                        browser.execute_script("arguments[0].click();", page_next)
                        return self.fanye(browser, data)
                    else:
                        return data
                except: # 没有下一页
                    return data
            else:
                return data              
        except: # 没有期刊
            print("加载文献列表出问题")
            traceback.print_exc()
            return data
        
    def get_paper_list(self):
        '''爬取
        :param log 传入一个Log对象
        '''
        # 载入日志
        # 获取filename
        # 存在就不继续查看其内容
        # 更新日志
        pass
    
class SubjectConfig:
    '''
    主题过滤配置类
    主要从该类中获取主题以及构造检索式
    '''

    def __init__(self):
        '''
        初始化获得主题列表
        '''
        self.config = get_journal_config().get('subject_list')
    
    def get_subjects(self):
        '''
        获取所有主题以及格式化好的关键词
        '''
        subjects = []
        for key, value in self.config.items():
            subject = {}
            subject['name'] = value['name']
            subject['retreval_str'] = self.get_one_retreval(key)
            subjects.append(subject)
        return subjects


    
    def get_one(self, key):
        '''
        获取一个主题的所有信息
        '''
        try:
            return self.config[key]
        except:
            return False
    
    def get_one_retreval(self, key):
        '''
        获取某一个主题的检索表达式
        '''
        value = self.get_one(key)
        if value != False:
            keywords = value['keywords']
            if len(keywords) == 1:
                retreval_str = ''' SU = '{0}' '''.format(keywords[0])
            else: # 构造检索表达式
                retreval_str = "' + '".join(keywords)
                retreval_str = "'" + retreval_str + "'"
                retreval_str = "SU = " + retreval_str
            return retreval_str
        return False

    def get_one_subject_name(self, key):
        '''
        获取主题名称
        '''
        value = self.get_one(key)
        return value['name']

                



        
