from selenium import webdriver
'''
全局组件文件
应对不同将代码放到不同的环境的时候由于参数的设置所出现的偏差
比如webdriver中的配置选项
'''

def get_webdriver():
    '''
    获取webdriver
    '''
    # TO DO 从config.yaml中读取有关的配置作为参数穿进去
    browser = webdriver.Chrome() # 参数可能需要设置
    return browser