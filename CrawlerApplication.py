import urllib.request
import lxml.etree
from bs4 import BeautifulSoup
import re
import datetime
import time
import csv
import os

ITEMS_PAGE = 30
TIME_SLEEP = 5
API = "a3cde9e1462bb4d112bae6620ea9ac92"
CITY = ['jinan']
CITY_NAME = ['防城港市']

class Spider:
    def getContent(self, url):
        conn = urllib.request.urlopen(url)
        output = lxml.etree.HTML(conn.read())
        return output

    def saveContent(self, filePath, content):
        file_obj = open(filePath, 'w', encoding = 'UTF-8')
        file_obj.write(content)
        file_obj.close()

class Community:
    communtyPrice = ''
    communityLat = ''
    communityLng = ''
    communityName = ''
    communityAdd = ''
    communityTotalArea = ''
    communityTotalFamily = ''
    communityBuildYear = ''
    communityGreenRate = ''


def getResultFromJS(destStr):
    stringFind = str( soup.findAll(text = re.compile(destStr)) )
    #print(stringFind)
    strBegin = stringFind.find(destStr)
    #print("strBegin:", strBegin)

    count = 0
    posBegin = 0
    posEnd = 0
    for i in range(strBegin, len(stringFind)):
        if (stringFind[i] == '\''):
            count += 1
            if (count == 2):
                posBegin = i + 1
            if (count == 3):
                posEnd = i
                break

    #print(posBegin)
    #print(posEnd)
    resultStr = stringFind[posBegin: posEnd]
    print(resultStr)
    return resultStr

def getPrice(destStr):
    stringFind = str( soup.select("em[class=" + destStr + "]") )
    #print(stringFind)

    posBegin = stringFind.find(">")
    posEnd = stringFind.find("</em>")

    for i in range(posBegin, len(stringFind)):
        if (stringFind[i].isdigit()):
            posBegin = i
            break

    price = stringFind[posBegin : posEnd]
    print(price)
    return price

def getAddress(destStr):
    stringFind = str( soup.select("dd[class=" + destStr + "]") )
    #print(stringFind)

    posBegin = stringFind.find("<em>")
    posEnd = stringFind.find("</em>")

    address = stringFind[posBegin + 4 : posEnd]
    print(address)
    return address

def getBasicInformation(className, destStr):
    stringFind = str( soup.find_all('dl',class_ = className) )
    #print(stringFind)

    stringFind = stringFind[stringFind.find(destStr):]
    posBegin = stringFind.find("<dd>")
    posEnd = stringFind.find("</dd>")


    info = stringFind[posBegin + 4 : posEnd]
    print(info)
    return info

def getCommunityLink(html):
    soup = BeautifulSoup(html, "lxml")
    stringFind = str( soup.findAll(href = re.compile('community/view')) )
    #print(stringFind)

    #print("start")
    numList = [0]
    while ( len(stringFind) > 3):
        posBegin = stringFind.find('community/view/') + len('community/view/')
        stringFind = stringFind[posBegin:]
        posEnd = stringFind.find('/')
        num = stringFind[0 : posEnd]

        stringFind = stringFind[posEnd:]
        #print(posBegin)
        #print(posEnd)
        #print(num)

        if (num != numList[len(numList) - 1]) and num.isdigit():
            numList.append(num)

    del numList[0]
    # print(len(numList))
    # print(numList)

    for i in range(0 , len(numList)):
        numList[i] = "http://" + CITY[0] + ".anjuke.com/community/view/" + numList[i]

    print(numList)
    return numList

def getCommunityAmount(html, className, destStr):
    soup = BeautifulSoup(html, "lxml")
    stringFind = str( soup.find_all(class_ = className) )
    #print(stringFind)

    posBegin = 0
    posEnd = 0
    for i in range(0 , len(stringFind)):
        if stringFind[i].isdigit():
            posBegin = i
            break

    i = len(stringFind) - 1
    for i in range(len(stringFind) - 1, 0, -1):
        if stringFind[i].isdigit():
            posEnd = i
            break

    info = stringFind[posBegin : posEnd + 1]
    print(info)
    return int(info)

def writeToFile(dataContent, method):
    with open('./data/' + CITY[0] + '.csv', method, encoding = 'utf-8-sig') as f:
        writer = csv.writer(f, delimiter = ',')
        writer.writerow(dataContent)
    f.close()


url = "http://" + CITY[0] + ".anjuke.com/community/p"
totalPage = 1
ID = 1
dataOutput = []
headName = ['ID', '小区名', '地址', '经度', '纬度', '均价(元/平米)', '总住户', '总面积', '绿化率', '建造年代', 'LINK']
#dataOutput.append(headName)
#spider = Spider()
print("Start.......")

timeBegin = datetime.datetime.now()

#Find total pages
#print("test")
#os.remove("/data/" + CITY[0] + ".csv")
writeToFile(headName,"w")
totalNumHTML = urllib.request.urlopen("http://" + CITY[0] + ".anjuke.com/community/view").read()
totalPage = int(getCommunityAmount(totalNumHTML, "tit", "") / ITEMS_PAGE) + 1
print("Total pages: " + str(totalPage))

for pageNumber in range(1, totalPage + 1):
    currentURL = url + str(pageNumber)
    print("View page:", pageNumber, "   site:", currentURL)
    result = []

    communityList = getCommunityLink(urllib.request.urlopen(currentURL).read())

    data = [0]
    data[0] = ID

    for i in range(0, len(communityList)):
        print("#########################################################################")
        print("No.", ID)

        communityLink = urllib.request.urlopen(communityList[i]).read()
        soup = BeautifulSoup(communityLink, "lxml")
        data.append(getResultFromJS("comm_name"))
        data.append(CITY_NAME[0] + getAddress("comm-adres"))
        data.append(getResultFromJS("comm_lng"))
        data.append(getResultFromJS("comm_lat"))
        data.append(getPrice("comm-avg-price"))
        data.append(getBasicInformation("comm-r-detail float-r", "总户数"))
        data.append(getBasicInformation("comm-r-detail float-r", "总建面"))
        data.append(getBasicInformation("comm-r-detail float-r", "绿化率"))
        data.append(getBasicInformation("comm-r-detail float-r", "建造年代"))
        data.append(communityList[i])

        ID += 1
        dataOutput += data
        writeToFile(data,"a")
        data.clear()
        data.append(ID)

        time.sleep(TIME_SLEEP)
        # if ID == 3:
        #     break

print("Start to write")


# with open('./data/' + CITY[0] + '.csv', 'w', encoding = 'utf-8-sig') as f:
#     writer = csv.writer(f, delimiter = ',')
#     writer.writerow(headName)
#     length = len(dataOutput)
#     for i in range(0, len(dataOutput),len(headName)):
#         writer.writerow(dataOutput[i : i + len(headName)])
#
# f.close()

timeEnd = datetime.datetime.now()

print("Time: " + str((timeEnd - timeBegin).seconds) + "s")
print("Success!")


#CITY = ["fangchenggang",'','','','','','','','','','','','']
#CITY_NAME = ['防城港市','济南市','青岛市','德州市','淄博市','潍坊市','烟台市','日照市','德州市','','']