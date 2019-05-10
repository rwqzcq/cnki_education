from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SubjectFilter:
    '''
    爬取某一主题下的论文
    '''
    def __init__(self, subject, start_year, end_year):
        '''
        构造方法
        
        :Args:
         - subject: 主题词
         - start_year: 开始年份
         - end_year: 结束年份
        '''
        self.subject = subject
        self.start_year = start_year
        self.end_year = end_year
        self.build_retreval()
    
    def build_retreval(self):
        '''
        创建检索式
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
            search_id = '#1_2 > a' # 专业检索标识 #\31 _2 > a 
            # search = browser.find_element_by_css_selector(search_id)
            search = browser.find_element_by_xpath('//*[@id="1_2"]/a')
            browser.execute_script("arguments[0].click();", search) # 点击切换到专业检索
            try:
                # time.sleep(5)
                input_id = 'expertvalue'
                # input = browser.find_element_by_id(input_id) # 找到检索式的框
                input = WebDriverWait(browser, 10).until(           
                                    EC.presence_of_element_located((By.ID, input_id)))

                input.send_keys(self.retreval_str) # 输入检索式
                try:
                    select_id = 'year_from'
                    select_from = browser.find_element_by_id(select_id) # 找到起始的年限
                    Select(select_from).select_by_value(self.start_year) # 选择起始年限
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
                                browser.switch_to.frame(content_frame_id)
                                try:
                                    ## 开始递归操作
                                    journal_lists = browser.find_elements_by_css_selector("a.fz14")
                                    if journal_lists: # 找到论文列表
                                        for journal in journal_lists:
                                            print(journal.get_attribute("href"))
                                    
                                except:
                                    print("没有论文列表")
                            except:
                                pass
                            
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
                            pass
                    except:
                        print("找不到cssci选项")
                        pass
                except:
                    print("找不到起始年")
                    pass
            except:
                print("找不到输入框")
                pass
        except:
            print("找不到检索标识")
            pass
        finally:
            browser.close()


    def get_paper_list(self):
        '''爬取
        :param log 传入一个Log对象
        '''
        # 载入日志
        # 获取filename
        # 存在就不继续查看其内容
        # 更新日志
        pass
    

subject = SubjectFilter('校园突发事件XXX', start_year = '2015', end_year = '2019')
subject.get()