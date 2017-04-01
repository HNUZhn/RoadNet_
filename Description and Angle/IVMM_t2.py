from getdata import *
from Class import *
from theFunctions import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt ##　　% matplotlib qt5
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import datetime
startTime = datetime.datetime.now()
#把采样点匹配到路网上，画出匹配的路网。
#存在的问题：路网不连续，存在间隔。匹配误差，未考虑行进方向

jsonURL = 'street2.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList,crossList)
froadList = GetData.getFRoadlist(roadList,0.0025,25)
fcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[0]
fsegmentList = GetData.getFsegmentlist(roadList,0.0025,25)
fjointList = GetData.getJointlist(fsegmentList, fcrosslist)



###最短距离算法
def findJointByCoordinate(C, jointList):  # 通过交叉点的坐标找出交叉点的ID
    for item in jointList:
        if item.coordinate == C:
            return item
    return False

            # 把Joint作为head或tail，添加到Segment的类里
def find_tJoint_byID(ID):
    for item in tJointList:
        if item.id == ID:
            return item

for item in fsegmentList:
    if item.Head == None:
        item.setHeadJoint(findJointByCoordinate(item.getHead(), fjointList))
    if item.Tail == None:
        item.setTailJoint(findJointByCoordinate(item.getTail(), fjointList))

tJointList = []
for item in fjointList:
    tJointList.append(tJoint(item))

# A*算法
def AStar(StartNodeID, EndNodeID):
    OpenList = []
    CloseList = []
    StartNode = find_tJoint_byID(StartNodeID)
    print (StartNode)
    EndNode = find_tJoint_byID(EndNodeID)

    # 内部函数
    def getOpenMinF(openlist):  # L是dict格式
        testList2 = sorted(openlist, key=lambda x: x.f, reverse=True)
        return testList2[-1]
        # 内部函数

    def get_length_byTwoID(s_c, s_p_c):  # L是dict格式
        length = 0
        for item in fsegmentList:
            if (s_c == item.getHead() and s_p_c == item.getTail()) or (
                    s_p_c == item.getHead() and s_c == item.getTail()):
                length = item.getLength()
        return length

    def h(s):  # 从结束点到Node的估计值h
        S = s.coordinate
        E = EndNode.coordinate
        if S != None and E != None:
            return ((S[0] - E[0]) ** 2 + (S[1] - E[1]) ** 2) ** 0.5
        else:
            print('警告，点找不到！！！')
            return False

    def g(s):  # 从出发点到Node点的最短路程 =  父节点的g + 该点到父节点的路段长
        if s.parent != None:
            return s.parent.f + get_length_byTwoID(s.coordinate, s.parent.coordinate)
        else:
            # print('警告，s.parent为空！！！')
            return float('inf')

    def f(s):  # f=g(n) + (abs(dx - nx) + abs(dy - ny))；   f(n)=g(n)+h(n)
        return h(s) + g(s)

    def printObjectList(ObjectList):
        ID = []
        for item in ObjectList:
            ID.append(item.id)
        print(ID)

    def reconstruct_path(EndNode):
        node = EndNode
        printNodeIDList = []
        while (node.parent != None):
            printNodeIDList.append(node.id)
            node = node.parent
        printNodeIDList.append(node.id)  # 把开始点也加进来！
        return printNodeIDList

    StartNode.set_g(0)
    StartNode.set_f(h(StartNode))
    OpenList.append(StartNode)

    while (len(OpenList) != 0):
        OpenList = sorted(OpenList, key=lambda x: x.f, reverse=True)  # 把Open表按f值从大到小排列，pop出最后一个值（最小值）
        printObjectList(OpenList)
        printObjectList(CloseList)
        tempO = OpenList.pop()  # 最小点N
        print(tempO.id, tempO.f, '---------------------')
        CloseList.append(tempO)

        if tempO.id == EndNode.id:
            return reconstruct_path(EndNode)

        for itemJointID, itemLength in tempO.getNeighborEdge():
            tempNode = find_tJoint_byID(itemJointID)
            if tempNode in CloseList:
                continue

            tentative_gScore = tempO.g + itemLength

            if (tempNode not in OpenList):
                # tempNode.set_parent(tempO)
                OpenList.append(tempNode)
            elif tentative_gScore >= tempNode.g:
                continue

            tempNode.set_parent(tempO)
            tempNode.set_g(tentative_gScore)
            tempNode.set_f(tentative_gScore + h(tempNode))
            print('tempO.id:', tempO.id, 'tempNode.id:', tempNode.id, 'tempNode.g:', tempNode.g, 'tempNode.f:',
                  tempNode.f)

    # print('警告，没找到通路！！！')
    return False

##测试A*
# StartID = 245
# EndID = 233
#
#
# #StartID = 402
# #EndID = 476
# #print('TRUE or FALSE:', AStar(StartID,EndID))
#
# ans = AStar(StartID,EndID)
# if ans == False:
#     printNodeIDList = [StartID,EndID]
# else:
#     printNodeIDList = ans
# print('ANS为',printNodeIDList)
####最短距离算法结束

###IVAM改进算法
def getCP(fsegmentList, P):
    segmentList = []
    for itemF in fsegmentList:
        if itemF.getDescription() is not None:
            segmentList.append(itemF)

    # w = 0.02 # 200m
    w = 0.0002  # 100m
    minD = []
    min_len = []
    resultList = []
    fmin_list = []
    for itemS in segmentList:
        minDlist = []
        tempHeadC = []
        temp1 = 0
        tempList1 = []
        for itemC in itemS.cordinations:
            if len(tempHeadC) != 0:
                # temp1 = PointToSegDist(tempHeadC, itemC, P)
                tempList1.append(PointToSegDist(tempHeadC, itemC, P))
            tempHeadC = itemC
        minD.append(min(tempList1))# 选在距离w范围内的数据
        minD.append(itemS)
        minDlist.append(minD)
        minD = []
        for mind in minDlist:
            fmin_list.append(mind)

    D2 = []
    resultList = []
    temp_minD = fmin_list[0][0]
    for data in fmin_list:
        if data[0]<temp_minD:
            temp_minD = data[0]

    if  temp_minD < w :
        D2 = [i for i in fmin_list if i[0]<w] #把小于w的都存入D2
    else :
        D2 = [i for i in fmin_list if i[0]==temp_minD ]
    #print(type(D2))
    if len(D2) > 0 :
        resultList = D2
        min_len.append(len(list(D2)))
    return resultList,min_len

def get_mindisandcordinations(P,seg):
    minD = []
    minD_C = []
    tempHeadC = []
    temp1 = 0
    tempList1 = []
    tempList2 = []
    tempList3 = []
    for itemC in seg.cordinations:
        if len(tempHeadC) != 0:
            tempList1.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[0])
            tempList2.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[1])
            tempList3.append([tempHeadC,itemC])
            # print(get_Distance_and_Coordinate(tempHeadC, itemC, P))
            # print(tempList2)
        tempHeadC = itemC
    minD = min(tempList1)
    minD_C= tempList2[tempList1.index(min(tempList1))]
    minD_app = tempList3[tempList1.index(min(tempList1))]

    return minD,minD_C,minD_app

def matchGPStoRoad(data,fsegmentlist,froadlist,angle):
    obxy = data.loc[:, ["Lon", "Lat", "Direct"]]
    dislist = []
    fslist = []
    obuselist = []
    segid = []
    segbid = []
    matchlist = []
    for ob_1 in obxy.values:
        cpob_1 = getCP(fsegmentlist,ob_1[0:2])
        if (len(cpob_1[0])) == 0:
            print("分类出错")
            break
        checklist = []
        for i in range(len(cpob_1[0])):
            fcplist = []
            cpseg_1 = cpob_1[0][i][1]
            direct_1 = ob_1[2]
            angle_1 = cpseg_1.getScore()[0]
            meanlist = [angle_1-360,angle_1,angle_1+360]
            bid = cpseg_1.getbID()
            for ri in froadlist:
                son = ri.getSonRoads()
                for rison in son:
                    if rison.getID() == bid:
                        if len(son) == 1:
                            meanlist.append(angle_1 - 180)
                            meanlist.append(angle_1 + 180)
            # if direct_1 == 0:
            #     direct_1 =360
            for m_1 in meanlist:
                if abs(direct_1 - m_1)<angle:
                    if abs(m_1 - angle_1)==180:
                        fcplist.append("-")
                        fcplist.append(cpob_1[0][i])
                    else:
                        fcplist.append("+")
                        fcplist.append(cpob_1[0][i])
                    checklist.append(fcplist)
        if checklist != []:
            if len(checklist)>1:
                mindis = checklist[0][1][0]
                minuse = checklist[0][1]
                minfs = [checklist[0][0], minuse[1]]
                minsegid = minuse[1].getID()
                minsegbid = minuse[1].getbID()
                matchC = get_mindisandcordinations(ob_1[0:2], minuse[1])[1]
                for check_data in checklist:
                    if check_data[1][0]<mindis:
                        mindis = check_data[1][0]
                        minuse = check_data[1]
                        minfs = [check_data[0], minuse[1]]
                        minsegid = check_data[1][1].getID()
                        minsegbid = check_data[1][1].getbID()
                        matchC = get_mindisandcordinations(ob_1[0:2],minuse[1])[1]

                fslist.append(minfs)
                obuselist.append(minuse)
                segid.append(minsegid)
                segbid.append(minsegbid)
                dislist.append(mindis)
                matchlist.append(matchC)

            else:
                minuse = checklist[0][1]
                mindis = minuse[0]
                minfs = [checklist[0][0], minuse[1]]
                minsegid = minuse[1].getID()
                minsegbid = minuse[1].getbID()
                matchC = get_mindisandcordinations(ob_1[0:2], minuse[1])[1]

                fslist.append(minfs)
                obuselist.append(minuse)
                segid.append(minsegid)
                segbid.append(minsegbid)
                dislist.append(mindis)
                matchlist.append(matchC)

        else:
            minfs = []
            minuse = []
            minsegid = None
            minsegbid = None
            mindis = None
            matchC = []

            fslist.append(minfs)
            obuselist.append(minuse)
            segid.append(minsegid)
            segbid.append(minsegbid)
            dislist.append(mindis)
            matchlist.append(matchC)
        # print (len(segid))
    return  obuselist,segid,segbid,fslist,dislist,matchlist

###IVAM算法结束
##去重函数
def toRepeat(list):
    list_1 = []
    for list_data in list:
        if list_data not in list_1:
            list_1.append(list_data)
    return list_1

def compare(seg1,seg2):
    if seg1.getID() == seg2.getID():
        return True
    else:return False


##可视化数据选取##
pf = pd.read_csv('street_SZ.csv')
obdata = pf[pf['ObjectID'] == 117750]
obdata_26 = obdata[obdata['Day']==31]
obdata_useful = obdata_26[obdata_26['Hour'] == 17]
obdata_useful = obdata_useful.sort_values(by =['Hour','Min','Sec'])
obdata_useful = obdata_useful[obdata_useful['Speed'] != 0]
###

###IVAM算法应用
want = matchGPStoRoad(obdata_useful,fsegmentList,froadList,30)
obuselist = want[0]
fs_list = toRepeat(want[3])
fslist = [i for i in fs_list if i != []]
matchlist = [i for i in want[5] if i != []]
print ("1:",len(obuselist),toRepeat(obuselist))
print ("2:",len(fslist),fslist)
print ("3:",len(want[3]),want[3])
print(len(want[4]),want[4])
print(len(want[5]),want[5])

#匹配子路段可视化
for usedata in fslist:
    if usedata != []:
        cpobseg = usedata[1]
        LonXc = list(zip(*cpobseg.cordinations))[0]
        LatYc = list(zip(*cpobseg.cordinations))[1]
        plt.plot(LonXc, LatYc, c='r', linestyle='-', label='Road', linewidth=5, alpha=0.7)

###
##A*应用及可视化
def getStartEndList(fslist):
    listsetemp = []
    for i in range(len(fslist)-1):
        if not compare(fslist[i][1],fslist[i + 1][1]):
            if fslist[i][0] == '+':
                StartID = findJointByCoordinate(fslist[i][1].getTail(),fjointList).getID()
            else:
                StartID = findJointByCoordinate(fslist[i][1].getHead(), fjointList).getID()
            if fslist[i + 1][0] == '+':
                EndID = findJointByCoordinate(fslist[i + 1][1].getHead(),fjointList).getID()
            else:
                EndID = findJointByCoordinate(fslist[i + 1][1].getTail(), fjointList).getID()
            if StartID == EndID:
                continue
            else:
                se = [StartID,EndID]
                listsetemp.append(se)
    list_se = toRepeat(listsetemp)
    return list_se

list_se = getStartEndList(fslist)
print (list_se)

##A*匹配Joint点
def getAStarmatchJoint(list_se):
    printNodeIDListlist = []
    for data_se in list_se:
        ans = AStar(data_se[0], data_se[1])
        print ("ASN 为",ans)
        if ans == False:
            printNodeIDList = [data_se[0], data_se[1]]
        else:
            printNodeIDList = ans
        printNodeIDListlist.append(printNodeIDList)
    return printNodeIDListlist

printNodeIDListlist = getAStarmatchJoint(list_se)

##A*匹配Joint可视化
for NodeIDList in printNodeIDListlist:
    for itemID in NodeIDList:
        for itemJ in fjointList:
            if itemJ.id == itemID:
                plt.scatter(itemJ.coordinate[0], itemJ.coordinate[1], c='g', s=90, marker='o', alpha=0.9, edgecolors='none')
##A*匹配Segment可视化
addseglist = []
for NodeIDList_2 in printNodeIDListlist:
    for i in range(len(NodeIDList_2)-1):
        for itemS in fsegmentList:
            headC = find_tJoint_byID(NodeIDList_2[i]).coordinate
            tailC = find_tJoint_byID(NodeIDList_2[i+1]).coordinate
            if ((itemS.getHead() == headC) & (itemS.getTail() == tailC))  | ((itemS.getTail() == headC) & (itemS.getHead() == tailC)):
                LonXs = list(zip(*itemS.cordinations))[0]
                LatYs = list(zip(*itemS.cordinations))[1]
                plt.plot(LonXs, LatYs, c='m', linestyle='-', label='Road', linewidth=5, alpha=0.8)
                if ((itemS.getHead() == headC) & (itemS.getTail() == tailC)):
                    addseglist.append(["-",itemS])
                elif ((itemS.getTail() == headC) & (itemS.getHead() == tailC)):
                    addseglist.append(["+", itemS])
print(addseglist)

def complete(a,b):
    def gethead(c):
        signal = c[0]
        if signal == "+":
            head = c[1].getHead()
            tail = c[1].getTail()
        else:
            head = c[1].getTail()
            tail = c[1].getHead()
        return head

    def gettail(d):
        signal = d[0]
        if signal == "+":
            head = d[1].getHead()
            tail = d[1].getTail()
        else:
            head = d[1].getTail()
            tail = d[1].getHead()
        return tail

    # finnallist = a
    # for i in range(len(a)-1):
    #     tail = gettail(a[i])
    #     head_next = gethead(a[i+1])
    #     print (tail,head_next)
    #     if tail != head_next:
    #         print("不相等",tail, head_next)
    #         for seg_b in b:
    #             head_b = gethead(seg_b)
    #             tail_b = gettail(seg_b)
    #             if tail == head_b:
    #                 print(a[i][1].getID(),seg_b[1].getID())
    #                 a_index = finnallist.index(a[i])
    #                 finnallist.insert(a_index+1,seg_b)
    #                 b.remove(seg_b)
    #                 tail = tail_b
    #             if tail == head_next:
    #                 break
    #     else:continue

    for i in range(len(a)+len(b)-1):
        tail = gettail(a[i])
        head_next = gethead(a[i+1])
        # print (tail,head_next)
        if tail != head_next:
            # print("不相等",tail, head_next)
            for seg_b in b:
                head_b = gethead(seg_b)
                tail_b = gettail(seg_b)
                if tail == head_b:
                    print(a[i][1].getID(),seg_b[1].getID())
                    a.insert(i+1,seg_b)
                    b.remove(seg_b)
                    tail = tail_b
                if tail == head_next:
                    break
        else:continue
    finnallist = a
    return finnallist

finnallist = complete(fslist,addseglist)
print (len(finnallist),finnallist)
# for fi in finnallist:
#     print ([fi[1].getID(),fi[1].getHead(),fi[1].getTail()])

###路网可视化
## 画图部分
# 画路网
for item in fsegmentList:
    LonX = list(zip(*item.cordinations))[0]
    LatY = list(zip(*item.cordinations))[1]
    plt.plot(LonX, LatY, c='k', linestyle='-', label='Road', linewidth=2, alpha=0.5)
    plt.text((item.getHead()[0] + item.getTail()[0]) / 2, (item.getHead()[1] + item.getTail()[1]) / 2, item.getID(), color='y', alpha=0.5)

# 画交叉点
for itemJ in fjointList:
    plt.scatter(itemJ.coordinate[0], itemJ.coordinate[1], c='b', s=20, marker='o', alpha=0.4, edgecolors='none')
    # plt.text(itemJ.coordinate[0], itemJ.coordinate[1], itemJ.getID(),color='y', alpha=0.5)

#画GPS采样点
plt.scatter(obdata_useful['Lon'],obdata_useful['Lat'],s = 50,c = 'b',marker='o', alpha=0.9, edgecolors='none')

#画GPS匹配点
for matchpoint in matchlist:
    plt.scatter(matchpoint[0],matchpoint[1],s = 50 , c = 'c',marker='o', alpha=0.9, edgecolors='none')

xmajorFormatter = FormatStrFormatter('%.3f')  # 设置x轴标签文本的格式
ax = plt.gca()
ax.xaxis.set_major_formatter(xmajorFormatter)
ax.yaxis.set_major_formatter(xmajorFormatter)
plt.grid(True)
endTime = datetime.datetime.now()
print('本次程序运行时间为：', endTime-startTime)

plt.show()

print("画图完毕！")