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
            resList.append([itemJson['user']['uid'], itemJson['user']['uname'],itemJson['item']['content'], item['desc']['dynamic_id'], item['desc']['user_profile']['info']['face']])

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
    url = 'https://api.vc.bilibili.com/dynamic_repost/v1/dynamic_repost/repost_detail?dynamic_id=' + '613698174599991792'
    # 539142451483532317
    repostList = GetPagesCycle(url)#list(dict.fromkeys(GetPagesCycle(url)))
    #print("what")
    print(repostList)
    print('成功获取转发列表')

    filename = str(time.time())+"-alluid.txt"
    htmlname = str(time.time())+"-alluid.html"
    with io.open(filename, mode="w", encoding="utf-8") as resulttxt:
        for repost in sorted(repostList, key = lambda x: x[0]):
            resulttxt.write(str(repost)+"\n")
            
    with io.open(htmlname, mode="w", encoding="utf-8") as resulttxt:
        for repost in sorted(repostList, key = lambda x: x[0]):
            content = ""
            content = content+"<img src=\""+str(repost[4])+"\" alt=\"icon\" width=\"50\" height=\"50\">"
            content = content+" <a href=\""+"https://space.bilibili.com/"+str(repost[0])+"\">@"+repost[1]+"</a>"
            content = content+" <a href=\""+"https://t.bilibili.com/"+str(repost[3])+"\">: "+repost[2]+"</a>"+"<br>\n"
            resulttxt.write(content)
            
#loop_func(outFunc, 3600)

#print('Bilibili转发抽奖工具v1.0')
#print('Bilibili@鱼丸子_Official')

import ast
contents = []
with io.open("1642003402.784791-alluid.txt", mode="r", encoding="utf-8") as resulttxt:
    for line in resulttxt:
        contents.append(ast.literal_eval(line))

blacklist = set([
    293576070,
    413786,
    344325,
    15545025,
    27720812,
    2132319003,
    1853993736,
    1838338376,
    1517041754,
    1207377499,
    1165326558,
    1106951963,
    629803217,
    629795456,
    589254527,
    562729115,
    551257525,
    544502983,
    544498034,
    544491443,
    544224471,
    544196386,
    519727586,
    485290332,
    401924460,
    386037883,
    347807948,
    312592127,
    277431464,
    87838475,
    45997238,
    341395,
    1601556885,
    23558595,
    455655628,
    375563845,
    15303339,
    701183481,
    1348946954,
    1442268815,
    12304722,
    25983717,
    512527836,
    1616337363,
    1753343192,
    392548100,

    1293512,
    2153159,
    7767026,
    10929094,
    18245838,
    32439451,
    41977858,
    83507642,
    154152832,
    167384932,
    454694390,
    498504575,
    506577251,
    602040637,
    615918898,
    647875179,
    1335074545,
    1574423224,
    603147329,
    269535734,
    10540393,
    25054527,
    28952738,
    41596583,
    232637244,
    441752144,
    479604172,
    603952011,
    687109267,
    1557685497,
    1651204149,
    1661352125,
    1835541458,
    2049928950,
    135163,
    1556839,
    1565416,
    3724748,
    309425785,
    514144282,
    5300917,
    5375934,
    5768986,
    4399372,
    2095252,
    174372339,
    13185238,
    402041416,
    438420242,

    ])

whiteList = set()

with io.open("fixed.txt", mode="r", encoding="utf-8") as resulttxt:
    for line in resulttxt:
        whiteList.add(int(line.strip()))
with io.open("fixed-nonFilter.txt", mode="r", encoding="utf-8") as resulttxt:
    for line in resulttxt:
        whiteList.add(int(line.strip()))

whiteList = whiteList - blacklist
with io.open("current.html", mode="w", encoding="utf-8") as resulttxt:
    for repost in sorted(contents, key = lambda x: x[0]):
        if repost[0] in whiteList:
            content = ""
            content = content+"<img src=\""+str(repost[4])+"\" alt=\"icon\" width=\"50\" height=\"50\">"
            content = content+" <a href=\""+"https://space.bilibili.com/"+str(repost[0])+"\">@"+repost[1]+"</a>"
            content = content+" <a href=\""+"https://t.bilibili.com/"+str(repost[3])+"\">: "+repost[2]+"</a>"+"<br>\n"
            resulttxt.write(content)
with io.open("current.txt", mode="w", encoding="utf-8") as resulttxt:
    for repost in sorted(contents, key = lambda x: x[0]):
        if repost[0] in whiteList:
            resulttxt.write(str(repost)+"\n")

blacklist = blacklist.union(whiteList)
with io.open("result.html", mode="w", encoding="utf-8") as resulttxt:
    for repost in sorted(contents, key = lambda x: x[2]):
        if not(repost[0] in blacklist):
            content = ""
            content = content+"<img src=\""+str(repost[4])+"\" alt=\"icon\" width=\"50\" height=\"50\">"
            content = content+" <a href=\""+"https://space.bilibili.com/"+str(repost[0])+"\">@"+repost[1]+"</a>"
            content = content+" <a href=\""+"https://t.bilibili.com/"+str(repost[3])+"\">: "+repost[2]+"</a>"+"<br>\n"
            resulttxt.write(content)
userUid = set()
for repost in contents:
    userUid.add(repost[0])


userUid = userUid - blacklist
#generateNum = int(input('输入随机数量'))
uidResult = []
print('获取到的用户')
uidResult = list(userUid)
random.shuffle(uidResult)

uidResult = uidResult[0:50]
print(len(uidResult))

repostUserList = []
for repost in contents:
    if repost[0] in  uidResult:
        repostUserList.append(repost)

with io.open("LuckyResult.html", mode="w", encoding="utf-8") as resulttxt:
    for repost in repostUserList:
        content = ""
        content = content+"<img src=\""+str(repost[4])+"\" alt=\"icon\" width=\"50\" height=\"50\">"
        content = content+" <a href=\""+"https://space.bilibili.com/"+str(repost[0])+"\">@"+repost[1]+"</a>"
        content = content+" <a href=\""+"https://t.bilibili.com/"+str(repost[3])+"\">: "+repost[2]+"</a>"+"<br>\n"
        resulttxt.write(content)


contents = []
with io.open("current.txt", mode="r", encoding="utf-8") as resulttxt:
    for line in resulttxt:
        contents.append(ast.literal_eval(line))
random.shuffle(contents)
contextString = "恭喜以下用户抽中键帽以及啪叽： "
for repost in contents[0:3]:
    contextString = contextString + " @"+repost[1]
contextString = contextString+"\n恭喜以下用户抽中啪叽： "
for repost in contents[3:-1]:
    contextString = contextString + " @"+repost[1]
print(contextString)

input("enter to exit")