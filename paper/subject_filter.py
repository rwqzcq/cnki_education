# 主题爬取

# 爬取某一个主题下的所有期刊论文
class SubjectFilter:
    '''
    '''
    def __init__(self, subject):
        self.subject = subject
    
    '''创建检索式
    '''
    def build_retreval(self):
        self.retreval_str = ''' SU = '{0}' '''.format(self.subject)
    
    '''爬取
    :param log 传入一个Log对象
    '''
    def get_paper_list(self):
        # 载入日志
        # 获取filename
        # 存在就不继续查看其内容
        # 更新日志
        pass
    

subject = SubjectFilter('校园突发事件')
