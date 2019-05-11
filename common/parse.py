# 解析函数

from urllib.parse import parse_qs, urlparse



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