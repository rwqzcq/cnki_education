from abc import abstractmethod,ABCMeta
import requests
from paper.paper_parse import get_paper_detail_without_content

class Paper(metaclass=ABCMeta):
    '''
    论文的抽象类
    '''
    @abstractmethod
    def get_paper_detail_without_content(self, filename):
        '''
        获取论文详情的抽象方法
        '''
        pass

class ApiPaper(Paper):
    '''
    通过API的方式抓取论文的相关数据
    '''

    def get_paper_detail_without_content(self, filename):
        '''
        获取论文详情
        '''
        source_url = '''http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename={0}'''.format(filename)
        try:
            page = requests.get(source_url)
            soup = BeautifulSoup(page.text, 'html.parser')
            paper = get_pure_detail_from_detail_page(soup, filename)
            if paper == False:
                print(filename + "--文献不存在")
                return False
            return paper
        except:
            print("打不开论文详情的链接")
            return False

class SeleniumPaper(Paper):
    '''
    通过模拟浏览器的方式获取论文的相关数据
    '''

    def get_paper_detail_without_content(self, filename):
        '''
        获取论文详情
        '''
        return get_paper_detail_without_content(filename)   

def get_paper_obj(obj_name):
    '''
    暴露给外部的接口
    '''
    if obj_name == 'selenium':
        return SeleniumPaper()
    if obj_name == 'api':
        return ApiPaper()
