import unittest
from common.journal_config import get_journal_config
import time
from db.journal_db import get_db_cursor

class TestCommon(unittest.TestCase):
    '''
    测试common目录下的所有函数
    '''

    def test_get_journal_config(self):
        '''
        测试配置文件函数
        '''
        path = get_journal_config().get('chrome_webdriver_path')
        self.assertEqual(False, path)

    def test_year_range(self):
        '''
        测试year_range
        '''
        year_range = get_journal_config().get('year_range')
        self.assertEqual([2019, 2018, 2017], year_range)

    def test_run_time(self):
        '''
        测试程序运行时间
        '''
        now = time.time()
        time.sleep(1)
        end = time.time()
        between = end-now

    def test_db_connect(self):
        '''
        测试数据库链接
        '''
        cursor = get_db_cursor()
        print(cursor)