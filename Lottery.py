import requests
from bs4 import BeautifulSoup
import json
import random
from threading import Timer
import time
import sys
import io

#Core Page
#https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id=265215506136622321

#获取单页的转发列表（20个）
#返回列表：[0]是return code，[1]是获取到的列表
def GetOnePage(url):
    resList = []

    response = requests.get(url)
    resJson = json.loads(response.text)

    #Return code, return 0 if reposters exist
    rescode = resJson['code']
    if (rescode > 0):
        has_more = 0
        offset = ""
    else:
        has_more = resJson['data']['has_more']
        if (has_more > 0):
            offset = str(resJson['data']['offset'])
        else:
            offset=""
     
    if rescode == 0:
        #获取所单页的转发元素
        items = resJson['data']['items']
        for item in items:
            itemJson = json.loads(item['card'])
            #定位到UID
            resList.append(itemJson['user']['uid'])

    return [has_more, rescode, offset, resList]

def GetPagesCycle(url):
    allUIDSet = []

    #获取第一页
    firstPageGet = GetOnePage(url)
    hasMore = firstPageGet[0]
    retCode = firstPageGet[1]
    offset = firstPageGet[2]
    allUIDSet += firstPageGet[3]
    offsetIndex = 20
    while retCode == 0 and hasMore == 1:
        #偏移量增加，生成下一页的url
        offsetUrl = url + '&offset=' + str(offset)
        currentPage = GetOnePage(offsetUrl)
        #print(currentPage)
        hasMore = currentPage[0]
        retCode = currentPage[1]
        offset = currentPage[2]
        allUIDSet += currentPage[3]
        
    return allUIDSet

#随机方法，传入UID列表
def GetOneLuckyDog(uidList):
    listSize = len(uidList)
    luckyNum = random.randint(0, listSize - 1)
    return uidList[luckyNum]

def loop_func(func, second):
 #每隔second秒执行func函数
    while True:
          func()
          time.sleep(second)

def outFunc():
    url = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id=' + '539142451483532317'
    # 539142451483532317
    repostList = list(dict.fromkeys(GetPagesCycle(url)))
    #print("what")
    print(repostList)
    print('成功获取转发列表')

    filename = str(time.time())+"-alluid.txt"
    with io.open(filename, mode="w") as resulttxt:
        for useruid in repostList:
            resulttxt.write(str(useruid)+"\n")
          
print('Bilibili转发抽奖工具v1.0')
print('Bilibili@鱼丸子_Official')
  
loop_func(outFunc, 60)

def random(repostList):
    generateNum = int(input('输入随机数量'))

    print('获取到的用户')
    for i in range(0, generateNum):
        uidGet = GetOneLuckyDog(repostList)
        userPageUrl = 'https://space.bilibili.com/' + str(uidGet)
        print(userPageUrl)

    input()
