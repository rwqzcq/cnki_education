# 数据库操作
import pymysql
import pymysql.err
import yaml
import os
from common.journal_config import get_journal_config
import traceback

def get_db_cursor():
    '''
    获取数据库实例
    '''
    config = get_journal_config()
    db_config = config.get('db')
    db = pymysql.connect(db_config['host'],db_config['username'],db_config['password'],db_config['db_name'], charset='utf8')
    cursor = db.cursor()
    return cursor

def singleton(cls):
    '''
    数据库装饰器
    https://segmentfault.com/a/1190000016497271#articleHeader3
    '''
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]
    return inner

@singleton
class JournalDb:
    '''
    数据库操作
    '''
    db = None
    cursor = None
    
    def __init__(self):
        '''
        初始化链接数据库
        '''
        config = get_journal_config()
        db_config = config.get('db')
        try:
            JournalDb.db = pymysql.connect(db_config['host'],db_config['username'],db_config['password'],db_config['db_name'], charset='utf8') 
            JournalDb.cursor = JournalDb.db.cursor()
        except:
            print("数据库连接失败")
        finally:
            self.original_link = db_config['original_link']

    def insert_into_originallink(self, paper):
        '''
        一条一条插入到主要的内容表中

        '''
        sql = '''
            insert into `{0}`
            (
                `SHORT_DESC`, `TITLE`,  
                `CONTENT`, `SOURCE`, `RELEASE_DATETIME`, 
                `ISSN`, `SEARCH_WORDS_NAME`, `ORIGINAL_LINK`,
                `SUBJECT_TYPE`,`SOURCE_REAL`
            )
            values
            (
                %s, %s, 
                %s, %s, %s,
                %s, %s, %s,
                %s, %s
            )
        '''.format(self.original_link)
        try:
            subject_md5 = get_journal_config().get('subject_md5')
            content = self.build_content(paper['keywords'], paper['abstract'])
            bind_param = (
                paper['id'], paper['title'], 
                content, paper['perio'], paper['juanhao'],
                paper['issn'], paper['subject'], paper['original_url'],
                subject_md5, '学术期刊'
            )
            JournalDb.cursor.execute(sql, bind_param)
            JournalDb.db.commit()
        except Exception:
            JournalDb.db.rollback()
            traceback.print_exc()
            return False
        return True

    def insert_into_originallink_multi(self, paper_list):
        '''
        一次性向内容表中插入多条数据

        :Args:
         - paper_list 一个列表
        '''
        sql = '''
            insert into `{0}`
            (
                `SHORT_DESC`, `TITLE`,  
                `CONTENT`, `SOURCE`, `RELEASE_DATETIME`, 
                `ISSN`, `SEARCH_WORDS_NAME`, `ORIGINAL_LINK`,
                `SUBJECT_TYPE`,`SOURCE_REAL`
            )
            values
            (
                %s, %s, 
                %s, %s, %s,
                %s, %s, %s,
                %s, %s
            )
        '''.format(self.original_link)
        bind_params = []
        subject_md5 = get_journal_config().get('subject_md5')
        for paper in paper_list: # 遍历每一篇paper
            content = self.build_content(paper['keywords'], paper['abstract'])
            bind_param = (
                paper['id'], paper['title'], 
                content, paper['perio'], paper['juanhao'],
                paper['issn'], paper['subject'], paper['original_url'],
                subject_md5, '学术期刊'
            )
            bind_params.append(bind_param)
        try:
            JournalDb.cursor.executemany(sql, bind_params)
            JournalDb.db.commit()
        except:
            JournalDb.db.rollback()
            traceback.print_exc()
            return False
        return True

    def build_content(self, keywords, abstract):
        '''
        构造content字段
        '''
        keywords = keywords.replace(' ', '').replace("\n", '')
        content = '关键词 ' + keywords + '摘要 ' + abstract # "\n" + 
        return content
    
    def get_all_filename_of_one_subject(self, subject_name):
        '''
        获取所有的制定类型的期刊ID用来去重

        :Args:
         - subject_name: 类型名称
        
        :Returns:
         - list
        '''
        sql = '''
            select `SHORT_DESC`
            from `{0}`
            where `SEARCH_WORDS_NAME` = %s
        '''.format(self.original_link)
        try:
            JournalDb.cursor.execute(sql, (subject_name))
            results = JournalDb.cursor.fetchall() # 返回一个tuble
            if len(results) == 0:
                return False
            results = list(results)
            filename = []
            for i in results:
                filename.append(i[0])
            return filename
        except:
            JournalDb.db.rollback()
            traceback.print_exc()
            return False

    def __del__(self):
        '''
        析构函数，对象销毁的时候就断开数据库的链接
        '''
        JournalDb.db.close() 

