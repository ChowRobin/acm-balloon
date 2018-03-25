import requests
import http.cookiejar
import re
import os
from bs4 import BeautifulSoup
import pickle
try:
    from person import person
except:
    from api.person import person

class balloonSpider:
    def __init__(self, contestId=110, username=None, password=None):
        self.contestId = contestId
        self.username = username
        self.password = password
        self.url = 'http://ccpc.ahu.edu.cn/ContestRanklist.aspx?cid=' + str(contestId)
        self.headers = {
            'Connection': 'keep-alive',
            # 'Referer': '',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36'
        }
        self.session = requests.session()
        self.session.cookies = http.cookiejar.LWPCookieJar(filename='cookie')

    def login(self):
        loginUrl = 'http://ccpc.ahu.edu.cn/Login.aspx'
        res = self.session.get(loginUrl)
        soup = BeautifulSoup(res.text, 'html.parser')
        __VIEWSTATE = soup.find('input', id='__VIEWSTATE').get('value')
        __VIEWSTATEGENERATOR = soup.find('input', id='__VIEWSTATEGENERATOR').get('value')
        __EVENTVALIDATION = soup.find('input', id='__EVENTVALIDATION').get('value')
        loginData = {
            '__VIEWSTATE': __VIEWSTATE,
            '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
            '__EVENTVALIDATION': __EVENTVALIDATION,
            'TUsername': self.username,
            'TPassword': self.password,
            'Button1': '登 录'
        }
        try:
            self.headers['Referer'] = loginUrl
            self.session.post(loginUrl, data=loginData, headers=self.headers)
            self.session.cookies.save()
        except:
            print("login failed")


    def crawl(self):
        self.login()
        self.headers['Referer'] = 'http://ccpc.ahu.edu.cn/ContestProblemSet.aspx?cid='+str(self.contestId)
        res = self.session.get(self.url, headers=self.headers)
        return self.parse(res.text)

    # return [{xh, name, aclist:[id1,id2,id3...]}]
    def parse(self, res):
        # print(res)
        res1 = re.findall('showcranklist(.*);', res)

        _list = []
        for r in res1:
            tmp = r.split(',')
            name = tmp[4].strip("'")
            xh = tmp[3].strip("'")
            tmp1 = re.search('Array(.*)', r).group(1)
            tlist = tmp1.split(',')
            num = 0
            aclist = []
            for t in tlist:
                num += 1
                if ':' in t:
                    aclist.append(num)
            # print(xh, name, aclist)
            if len(aclist) > 0:
                _list.append({
                    'xh': xh,
                    'name': name,
                    'aclist': aclist
                })
        return _list

    def init(self):
        _path = os.getcwd()
        if not _path.endswith('/api'):
            _path += '/api'
        with open(_path+'/str', 'r') as f:
            return self.parse(f.read())

def main():
    spider = balloonSpider()
    print(spider.crawl())

if __name__ == '__main__':
    main()