import unittest
from paper.subject_filter import SubjectFilter, SubjectConfig
from log.log_transform import LogTransform
from log.log_daily import DailyLog


class TestLog(unittest.TestCase):
    '''
    日志文件测试类
    '''

    def test_all_into_year(self):
        '''
        测试日志文件转化模块
        '''
        transform = LogTransform()
        subject_config = SubjectConfig()
        subject_list = subject_config.get_subjects()
        for subject in subject_list:
            print(subject['name'] + '---')
            result = transform.all_into_one_year(subject_name=subject['name'])
            self.assertEqual(True, result)

    def test_daily_log(self):
        '''
        测试爬取日志
        '''
        daily_log = DailyLog()
        daily_log.format_data(total = 15, updated = 9)
        
