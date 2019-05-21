from queue import Queue
from paper.subject_filter import SubjectFilter, SubjectConfig

class SubjectQueue():

    def __init(self):
        pass

def get_subject_queue():
    '''
    获取主题队列
    '''
    subject_config = SubjectConfig()
    subject_list = subject_config.get_subjects()
    subject_num = len(subject_list)
    subect_queue = Queue(subject_num)
    # 放入1~10的数字，先进先出
    for subject in subject_list:
        subect_queue.put(subject)
    return subect_queue