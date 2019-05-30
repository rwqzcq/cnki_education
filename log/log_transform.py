from log.log import CnkiLog
from log.year_log import CnkiYearLog
from common.parse import parse_from_filename

class LogTransform():
    def all_into_one_year(self, subject_name):
        '''
        将所有的年限日志转换为一个一个年份的
        '''
        cnki_log = CnkiLog(log_name = subject_name, full_name = subject_name)
        log = cnki_log.get_log() # 获取当前的日志文件
        if log == False:
            print("没有日志文件")
            return False
        year_list = []
        new_log = {}
        # 重新组织
        for key,value in log.items():
            year = parse_from_filename(key)['year']
            year = str(year)
            # new_log[year][value['filename']] = value
            if year in year_list:
                new_log[year][value['filename']] = value
            else:
                year_list.append(year)
                new_log[year] = {} # 一定要声明一个空的dict 否则会报错
                new_log[year][value['filename']] = value
        # 转化日志
        for key, value in new_log.items():
            cnki_year_log = CnkiYearLog(subject_name, key)
            cnki_year_log.write_log(value)