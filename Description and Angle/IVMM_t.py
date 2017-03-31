#把采样点匹配到路网上，画出匹配的路网。
#存在的问题：路网不连续，存在间隔。匹配误差，未考虑行进方向
import math
from readdata import *
from theFunctions import *
from Class import *
# from trajectory_filter_1 import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt ##　　% matplotlib qt5
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import datetime
startTime = datetime.datetime.now()


# 查询离范围w内的候选的CP集，每条符合条件的segment i对应一个CPi
# 斜对角的0.05距离大约对应528.7m      0.01~105.74m
# 当最小值小于CR时，最多选择CRn（3~10,）5个满足条件的候选点（小于CR）；
# 当最小值大于或等于CR时，仅选择最小值对应的优选点做候选集。

def getCP2(fsegmentList, P):
    segmentList = []
    for itemF in fsegmentList:
        if itemF.getDescription() is not None:
            segmentList.append(itemF)
    # w = 0.02 # 200m
    w = 0.00015  # 100m
    minD = []
    min_len = []
    resultList = []
    for itemS in segmentList:
        tempHeadC = []
        temp1 = 0
        tempList1 = []
        for itemC in itemS.cordinations:
            if len(tempHeadC) != 0:
                # temp1 = PointToSegDist(tempHeadC, itemC, P)
                tempList1.append(PointToSegDist(tempHeadC, itemC, P))
            tempHeadC = itemC
        minD.append(min(tempList1))# 选在距离w范围内的数据

    D2 = []
    resultList = []
    temp_minD = min(minD)
    if  temp_minD < w :
        c = np.array(minD)
        D2 = c[c<w] #把小于w的都存入D2
    else :
        D2 = [temp_minD]
    #print(type(D2))
    if len(D2) > 0 :
        resultList = D2
        min_len.append(len(list(D2)))
    return resultList,min_len

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

def get_min_CP(fsegmentList, P):
    # w = 0.02 # 200m
    w = 0.1  # 100m
    minD = []
    minD_C = []
    tempID_List = []
    temp_min_segmentID = []
    temp_minDC = []
    min_len = []
    resultList = []
    segmentList = []
    for itemF in fsegmentList:
        if itemF.getDescription() is not None:
            segmentList.append(itemF)

    for itemS in segmentList:
        tempHeadC = []
        temp1 = 0
        tempList1 = []
        tempList2 = []
        for itemC in itemS.cordinations:
            if len(tempHeadC) != 0:
                # temp1 = PointToSegDist(tempHeadC, itemC, P)
                tempList1.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[0])
                tempList2.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[1])

                # print(get_Distance_and_Coordinate(tempHeadC, itemC, P))
                # print(tempList2)
            tempHeadC = itemC
        minD.append(min(tempList1))
        minD_C.append(tempList2[tempList1.index(min(tempList1))])
        tempID_List.append(itemS.id)

    temp_minD = min(minD)
    temp_minDC = minD_C[minD.index(temp_minD)]
    temp_min_segmentID = tempID_List[minD.index(temp_minD)]

    return temp_minD,temp_minDC,temp_min_segmentID
###A*加入
# 查询离P点最近的子路段Segment

def findJointByCoordinate(C, jointList):  # 通过交叉点的坐标找出交叉点的ID
    for item in jointList:
        if item.coordinate == C:
            return item

            # 把Joint作为head或tail，添加到Segment的类里
def find_tJoint_byID(ID):
    for item in tJointList:
        if item.id == ID:
            return item

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

###A*到此
print('开始')
# trajectory_GS = [[np.random.normal(i[0],1),np.random.normal(i[1],1)] for i in trajectory1]
# # print(trajectory1)
# # print(trajectory_GS)
# trajectory_CP = []
# for item in trajectory_GS:
#     trajectory_CP.append(get_min_CP(segmentList, item)[1])
#     # print(get_min_CP(segmentList, item))

import pandas as pd
import matplotlib.pyplot as plt
pf = pd.read_csv('street_SZ.csv')
obdata = pf[pf['ObjectID'] == 117750]
obdata_26 = obdata[obdata['Day']==31]
obdata_useful = obdata_26[obdata_26['Hour'] == 17]
obdata_useful = obdata_useful.sort_values(by =['Hour','Min','Sec'])
obdata_useful = obdata_useful[obdata_useful['Speed'] != 0]
obxy = obdata_useful.loc[ :,["Lon","Lat","Direct"]]


obuselist = []
for ob_1 in obxy.values:
    cpob_1 = getCP(fsegmentList,ob_1[0:2])
    checklist = []
    for i in range(len(cpob_1[0])):
        fcplist = []
        cpseg_1 = cpob_1[0][i][1]
        direct_1 = ob_1[2]
        angle_1 = cpseg_1.getScore()[0]
        meanlist = [cpseg_1.getScore()[0]]
        bid = cpseg_1.getbID()
        for ri in froadList:
            son = ri.getSonRoads()
            for rison in son:
                if rison.getID() == bid:
                    if len(son) == 1:
                        meanlist.append(angle_1 - 180)
                        meanlist.append(angle_1 + 180)
        if direct_1 == 0:
            direct_1 =360
        for m_1 in meanlist:
            if abs(direct_1 - m_1)<30:
                checklist.append(cpob_1[0][i])
    if checklist != []:
        if len(checklist)>1:
            mindis = checklist[0][0]
            minuse = checklist[0]
            for check_data in checklist:
                if check_data[0]<mindis:
                    mindis = check_data[0]
                    minuse = check_data
        else:minuse = checklist[0]
    else:minuse = []
    obuselist.append(minuse)

#去有用点的匹配子路段数据结构
fseg_uselist = []
fseg_ddlist = []
for ob_usedata in obuselist:
    if ob_usedata != []:
        fseg_data  = ob_usedata[1]
        fseg_ddlist.append(fseg_data)
for ob_dddata in fseg_ddlist:
    if ob_dddata not in fseg_uselist:
        fseg_uselist.append(ob_dddata)


for item in fsegmentList:
    if item.Head == None:
        item.setHeadJoint(findJointByCoordinate(item.getHead(), fjointList))
    if item.Tail == None:
        item.setTailJoint(findJointByCoordinate(item.getTail(), fjointList))

tJointList = []
for item in fjointList:
    tJointList.append(tJoint(item))


StartID = 245
EndID = 233


#StartID = 402
#EndID = 476
#print('TRUE or FALSE:', AStar(StartID,EndID))

ans = AStar(StartID,EndID)
if ans == False:
    printNodeIDList = [StartID,EndID]
else:
    printNodeIDList = ans
print('ANS为',printNodeIDList)
#
# for i in range(len(fseg_uselist)-1):
#     StartID = findJointByCoordinate(fseg_uselist[i].getTail(),jointList).getID()
#     EndID = findJointByCoordinate(fseg_uselist[i+1].getHead(),jointList).getID()
#     print(StartID,EndID)
# printNodeIDListlist = []
# for i in range(len(fseg_uselist)-1):
#     StartID = findJointByCoordinate(fseg_uselist[i].getTail(),jointList).getID()
#     EndID = findJointByCoordinate(fseg_uselist[i+1].getHead(),jointList).getID()
#     print (StartID,EndID)
#     ans = AStar(StartID, EndID)
#     print ("ASN 为",ans)
#     if ans == False:
#         printNodeIDList = [StartID, EndID]
#     else:
#         printNodeIDList = ans
#     printNodeIDListlist.append(printNodeIDList)
# print(printNodeIDListlist)
#
# for NodeIDList in printNodeIDListlist:
#     for itemID in NodeIDList:
#         for itemJ in jointList:
#             if itemJ.id == itemID:
#                 plt.scatter(itemJ.coordinate[0], itemJ.coordinate[1], c='g', s=90, marker='o', alpha=0.9, edgecolors='none')

for usedata in obuselist:
    if usedata != []:
        cpobseg = usedata[1]
        LonXc = list(zip(*cpobseg.cordinations))[0]
        LatYc = list(zip(*cpobseg.cordinations))[1]
        plt.plot(LonXc, LatYc, c='r', linestyle='-', label='Road', linewidth=5, alpha=0.7)

# for ob in obxy.values:
#     cpob = getCP(fsegmentList,ob[0:2])
#
#     for cpobf in cpob[0]:
#         angle = ob[2]##车的角度
#         cpobseg= cpobf[1]
#         mean = cpobseg.getScore()[0]#路的角度
#         meanangle = [cpobseg.getScore()[0]]
#         bid = cpobseg.getbID()
#         for ri in froadList:
#             son = ri.getSonRoads()
#             for rison in son:
#                 if rison.getID() == bid:
#                     if len(son) == 1:
#                         meanangle.append(mean-180)
#                         meanangle.append(mean+180)
#
#         # LonXc = list(zip(*cpobseg.cordinations))[0]
#         # LatYc = list(zip(*cpobseg.cordinations))[1]
#         # plt.plot(LonXc, LatYc, c='g', linestyle='-', label='Road', linewidth=5, alpha=0.5)
#         ##角度分析有待研究关于0与360
#         if angle==0:
#             angle = 360
#         for m in meanangle:
#             if angle-30 < m < angle + 30:
#                 LonXc = list(zip(*cpobseg.cordinations))[0]
#                 LatYc = list(zip(*cpobseg.cordinations))[1]
#                 plt.plot(LonXc, LatYc, c='r', linestyle='-', label='Road', linewidth=5, alpha=0.7)
# obcp = getCP(fsegmentList,obxy)

cp = getCP(fsegmentList,[114.058027 ,22.544823])#350
cp2 = getCP2(fsegmentList,[114.058027 ,22.544823])
plt.scatter(114.058027 ,22.544823,c='y',s=100)
for cpf in cp[0]:
    cpseg= cpf[1]
    # print(cpseg.getScore())
    # if 325 < cpseg.getScore()[0] < 375:
    LonXc = list(zip(*cpseg.cordinations))[0]
    LatYc = list(zip(*cpseg.cordinations))[1]
    plt.plot(LonXc, LatYc, c='g', linestyle='-', label='Road', linewidth=7, alpha=0.5)
    if 330 < cpseg.getScore()[0] < 390:
        LonXc = list(zip(*cpseg.cordinations))[0]
        LatYc = list(zip(*cpseg.cordinations))[1]
        plt.plot(LonXc, LatYc, c='m', linestyle='-', label='Road', linewidth=7, alpha=0.5)
# print (cp)
# print (cp2)



## 画图部分
# 画路网
for item in fsegmentList:
    LonX = list(zip(*item.cordinations))[0]
    LatY = list(zip(*item.cordinations))[1]
    plt.plot(LonX, LatY, c='k', linestyle='-', label='Road', linewidth=2, alpha=0.5)

# 画交叉点
for itemJ in fjointList:
    plt.scatter(itemJ.coordinate[0], itemJ.coordinate[1], c='b', s=20, marker='o', alpha=0.4, edgecolors='none')
    plt.text(itemJ.coordinate[0], itemJ.coordinate[1], itemJ.getID(),color='y', alpha=0.5)

plt.scatter(obdata_useful['Lon'],obdata_useful['Lat'],s = 50,c = 'b',marker='o', alpha=0.9, edgecolors='none')


xmajorFormatter = FormatStrFormatter('%.3f')  # 设置x轴标签文本的格式
ax = plt.gca()
ax.xaxis.set_major_formatter(xmajorFormatter)
ax.yaxis.set_major_formatter(xmajorFormatter)
plt.grid(True)
# plt.xlim(112.900, 113.050)  # set the xlim to xmin, xmax
# plt.ylim(28.120, 28.265)
# plt.subplots_adjust(left=0.08, bottom=0.08)
# plt.legend('Road1','Road2')
endTime = datetime.datetime.now()
print('本次程序运行时间为：', endTime-startTime)


plt.show()

print("画图完毕！")

