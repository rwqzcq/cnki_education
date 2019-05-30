# 解析函数

from urllib.parse import parse_qs, urlparse
import re


def parse_filename(url):
    '''
    从uri中解析出论文的id

    :Args:
     - url 相对路径
    '''
    # http://navi.cnki.net/Common/RedirectPage?sfield=FN&dbCode=CJFD&filename=JYYJ201902015&tableName=CJFDTEMP&url=
    redirect_url = 'http://navi.cnki.net/' + url
    redirect_url = url
    query_str = urlparse(redirect_url).query
    params = parse_qs(query_str)
    if params['filename']:
        cnki_str = params['filename'][0]
        return cnki_str
    else:
        print("解析fileName出错了!")
        return False

def parse_from_filename(filename):
    '''
    从filename中解析出有关的信息

    :Args:
     - filename: cnki唯一标识
    
    :returns:
     - dict
    '''
    journal_name = ''.join(re.split(r'[^A-Za-z].*', filename)) # issue可能会有字母 核心规则为以字母开头然后以数字结束 使用惰性匹配 遇到数字就停止匹配

    filename = filename.replace(journal_name, '')

    year = filename[0:4]
    issue = filename[4:6]
    xuhao = filename[6:]

    return {
        'journal_name' : journal_name,
        'year' : year,
        'issue' : issue,
        'xuhao' : xuhao
    }
