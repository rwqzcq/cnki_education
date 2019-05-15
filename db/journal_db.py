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
        插入到主要的内容表中
        '''
        sql = '''
            insert into `{0}`
            (
                `ID`, `TITLE`, `SHORT_DESC`, 
                `CONTENT`, `SOURCE`, `YEAR_AND_VOLUME_OR_PERIOD`, 
                `ISSN`, `SEARCH_WORDS_NAME`, `ORIGINAL_URL`
            )
            values
            (
                %s, %s, %s,
                %s, %s, %s,
                %s, %s, %s
            )
        '''.format(self.original_link)
        try:
            bind_param = (
                paper['id'], paper['title'], paper['abstract'],
                paper['content'], paper['perio'], paper['juanhao'],
                paper['issn'], paper['keywords'], paper['original_url']
            )
            JournalDb.cursor.execute(sql, bind_param)
            JournalDb.db.commit()
        except Exception:
            JournalDb.db.rollback()
            print("插入失败--ID重复!")
            # traceback.print_exc()
            return False
        return True

    def insert_into_originallink_multi(self, paper_list):
        '''
        一次性向内容表中插入多条数据

        :Args:
         - paper_list 一个列表
        '''
        '''
        插入到主要的内容表中
        '''
        sql = '''
            insert into `{0}`
            (
                `ID`, `TITLE`,  
                `CONTENT`, `SOURCE`, `YEAR_AND_VOLUME_OR_PERIOD`, 
                `ISSN`, `SEARCH_WORDS_NAME`, `ORIGINAL_URL`,
                `SUBJECT_TYPE`
            )
            values
            (
                %s, %s, 
                %s, %s, %s,
                %s, %s, %s,
                %s
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
                subject_md5
            )
            bind_params.append(bind_param)
        try:
            rows = JournalDb.cursor.executemany(sql, bind_params)
            JournalDb.db.commit()
        except Exception:
            JournalDb.db.rollback()
            print("插入失败--ID重复!")
            # traceback.print_exc()
            return False
        return True

    def build_content(self, keywords, abstract):
        '''
        构造content字段
        '''
        keywords = keywords.replace(' ', '').replace("\n", '')
        content = '关键词 ' + keywords + '摘要 ' + abstract # "\n" + 
        return content
    def __del__(self):
        '''
        析构函数，对象销毁的时候就断开数据库的链接
        '''
        JournalDb.db.close() 

