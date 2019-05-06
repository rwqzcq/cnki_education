import yaml
import os

def get_journal_config():
    '''
    获取配置文件
    '''
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    with open(config_path,'rb') as f:
        cont = f.read()
    config = yaml.load(cont)
    return config