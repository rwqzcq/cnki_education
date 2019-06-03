import unittest
from paper.subject_filter import SubjectFilter, SubjectConfig
from log.log_transform import LogTransform

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
            result = transform.all_into_one_year(subject_name = subject['name'])  
            self.assertEqual(True, result)
              