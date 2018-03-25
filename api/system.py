import requests
import re
from bs4 import BeautifulSoup
import pickle
import os
import sys
try:
    from api.person import person
    from api.spider import balloonSpider
except:
    from person import person
    from spider import balloonSpider

class system:
    def __init__(self, id=110, username=None, password=None):
        self.path = os.getcwd()
        if not self.path.endswith('/api'):
            self.path += '/api'
        # print(self.path)
        self.spider = balloonSpider(id, username, password)
        self.qnums = 8
        try:
            # print(os.path.exists(self.path+'/personData'))
            self.plist = pickle.load(open(self.path+'/personData', 'rb'))
            print("person'data load successful")
        except:
            print("person's data not found")
            self.plist = []
            self.initPersonData()
        try:
            # print(os.path.exists(self.path+'/balloonData'))
            self.id2color = pickle.load(open(self.path+'/balloonData', 'rb'))
            print("balloon'data load successful")
        except:
            print("balloon's data not found")
            self.id2color = {
                1: "红",
                2: "蓝",
                3: "黄",
                4: "橙",
                5: "绿",
                6: "青",
                7: "紫",
                8: "黑"
            }
        try:
            self.contestList = pickle.load(open(self.path+'/contestData', 'rb'))
            print("contest's data load successful")
        except:
            print("contest's data not found")
            self.contestList = [
                {'name': '测试赛', 'id': 110}
            ]
            pickle.dump(self.contestList, open(self.path+'/contestData', 'wb'))
        try:
            self.firstBlood = pickle.load(open(self.path+'/firstBloodData', 'rb'))
            print("first blood's data load successful")
        except:
            print("first blood's data not found")
            self.firstBlood = {}
            for i in range(1, self.qnums+1):
                self.firstBlood[i] = False
            pickle.dump(self.firstBlood, open(self.path+'/firstBloodData', 'wb'))

    def initPersonData(self):
        _list = self.spider.init()
        for p in _list:
            self.plist.append(person(p['name'], p['xh']))
        pickle.dump(self.plist, open(self.path+'/personData', 'wb'))

    def clearData(self):
        for p in self.plist:
            p.initStatus()
        pickle.dump(self.plist, open(self.path+'/personData', 'wb'))
        for i in range(1, self.qnums+1):
            self.firstBlood[i] = False
        pickle.dump(self.firstBlood, open(self.path+'/firstBloodData', 'wb'))

    def printPersonData(self):
        for p in self.plist:
            print(p.name, p.xh, p.position)

    def printBalloonData(self):
        for i in range(1, self.qnums):
            print(i, '=>', self.id2color[i])

    def getIdColor(self, id):
        if id in self.id2color.keys():
            return self.id2color[id]
        else:
            return None

    def setIdColor(self, id, color):
        self.id2color[id] = color
        pickle.dump(self.id2color, open(self.path+'/balloonData', 'wb'))

    def getPositionMsg(self):
        pm = []
        for p in self.plist:
            obj = {}
            obj['xh'] = p.xh
            obj['name'] = p.name
            obj['position'] = p.position
            pm.append(obj)
        return pm

    def setPositionMsg(self, form):
        for p in self.plist:
            p.position = form[p.xh]
        pickle.dump(self.plist, open(self.path+'/personData', 'wb'))

    def handleNewData(self, newList):
        for d in newList:
            for p in self.plist:
                if d['xh'] == p.xh:
                    for i in d['aclist']:
                        p.ac(i)
        pickle.dump(self.plist, open(self.path+'/personData', 'wb'))

    # return [{xh, position, color, id}] 
    def calMsg(self):
        msgList = []
        for p in self.plist:
            for i in range(1, self.qnums+1):
                if p.acStatus(i) and not p.balloonStatus(i):
                    msg = {
                        'xh': p.xh,
                        'name': p.name,
                        'position': p.position,
                        'color': self.getIdColor(i),
                        'id': i,
                        'fb': False
                    }
                    if not self.firstBlood[i]:
                        self.firstBlood[i] = True
                        msg['fb'] = True
                    msgList.append(msg)
        pickle.dump(self.firstBlood, open(self.path+'/firstBloodData', 'wb'))
        return msgList

    def getMsg(self):
        _list = self.spider.crawl()
        self.handleNewData(_list)
        return self.calMsg()

    def handleMsg(self, _dict):
        for p in self.plist:
            if p.xh in _dict.keys():
                for i in _dict[p.xh]:
                    p.getBalloon(int(i))
        pickle.dump(self.plist, open(self.path+"/personData", 'wb'))
    
    def getBalloonMsg(self):
        _list = []
        for i in range(1, self.qnums+1):
            _dict = {'id': i, 'color': self.id2color[i]}
            _list.append(_dict)
        return _list

    def setBalloonMsg(self, form):
        for i in range(1, self.qnums+1):
            self.id2color[i] = form[str(i)]
        pickle.dump(self.id2color, open(self.path+'/balloonData', 'wb'))

    def getContestName(self, id):
        for item in self.contestList:
            if item['id'] == id:
                return item['name']

    def getContestList(self):
        return self.contestList

    def delContest(self, id):
        for item in self.contestList:
            if item['id'] == id:
                self.contestList.remove(item)
        pickle.dump(self.contestList, open(self.path+'/contestData', 'wb'))

    def addContest(self, name, id):
        self.contestList.append({
            'name': name,
            'id': int(id)
        })
        pickle.dump(self.contestList, open(self.path+'/contestData', 'wb'))

if __name__ == '__main__':
    _system = system()
    _system.printPersonData()
    # print(_system.getMsg())
