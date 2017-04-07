from getdata import *
from Class import *
from theFunctions import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt ##　　% matplotlib qt5
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import datetime


jsonURL = 'street2.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList,crossList)
froadList = GetData.getFRoadlist(roadList,0.0025,25)
fcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[0]
fsegmentList = GetData.getFsegmentlist(roadList,0.0025,25)
fjointList = GetData.getJointlist(fsegmentList, fcrosslist)

startTime = datetime.datetime.now()
print("开始计时")

def get_min_CP(segmentList, P):
    # w = 0.02 # 200m
    w = 0.1  # 100m
    minD = []
    minD_C = []
    tempID_List = []
    temp_min_segmentID = []
    temp_minDC = []
    min_len = []
    resultList = []
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
        tempID_List.append(itemS)

    temp_minD = min(minD)
    temp_minDC = minD_C[minD.index(temp_minD)]
    temp_min_segmentID = tempID_List[minD.index(temp_minD)]

    return temp_minD,temp_minDC,temp_min_segmentID
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


P1 = (114.06308, 22.55861)
P2 = (114.06312, 22.55130)

getmin_p1 = get_min_CP(fsegmentList,P1)
getmin_p2 = get_min_CP(fsegmentList,P2)
print (getmin_p1,getmin_p2)
getJhead_p1 = findJointByCoordinate(getmin_p1[2].getHead(),fjointList).getID()
getJhead_p2 = findJointByCoordinate(getmin_p2[2].getHead(),fjointList).getID()
getJtail_p1 = findJointByCoordinate(getmin_p1[2].getTail(),fjointList).getID()
getJtail_p2 = findJointByCoordinate(getmin_p2[2].getTail(),fjointList).getID()
jlist = [getJhead_p1,getJtail_p1,getJhead_p2,getJtail_p2]
jlist_toAstar = [[jlist[0],jlist[2]],[jlist[0],jlist[3]],[jlist[1],jlist[2]],[jlist[1],jlist[3]]]
print (jlist_toAstar)
def getmin(listj,jointlist):
    def dis(A):
        dis = ((A[1][0]-A[0][0])**2+(A[1][1]-A[0][1])**2)**0.5
        return  dis

    def findJointByID(ID, jointList):  # 通过交叉点的坐标找出交叉点的ID
        for item in jointList:
            if item.id == ID:
                return item.coordinate
    clist = []
    for dataj in listj:
        idclist = []
        for dataid in dataj:
            dc = findJointByID(dataid, jointlist)
            idclist.append(dc)
        clist.append(idclist)
    print (clist)
    mind = dis(clist[0])
    minj = clist[0]
    for j in clist:
        if dis(j)<mind:
            mind = dis(j)
            minj = j
    idlist = []
    for cda in minj:
        minjid = findJointByCoordinate(cda,jointlist).getID()
        idlist.append(minjid)

    return  mind,minj,idlist

mindata = getmin(jlist_toAstar,fjointList)
print (mindata)

ans = AStar(mindata[2][0], mindata[2][1])
print("ASN 为", ans)
#可视化
for item in fsegmentList:
    LonX = list(zip(*item.cordinations))[0]
    LatY = list(zip(*item.cordinations))[1]
    plt.plot(LonX, LatY, c='k', linestyle='-', label='Road', linewidth=2, alpha=0.5)
    plt.text((item.getHead()[0] + item.getTail()[0]) / 2, (item.getHead()[1] + item.getTail()[1]) / 2, item.getID(), color='y', alpha=0.5)

for itemC in ans:
    for itemjoint in fjointList:
        if itemjoint.getID() == itemC:
            c = itemjoint.coordinate
            plt.scatter(c[0],c[1],c ='r',s=50)
# 画交叉点
for itemJ in fjointList:
    plt.scatter(itemJ.coordinate[0], itemJ.coordinate[1], c='b', s=20, marker='o', alpha=0.4, edgecolors='none')
    plt.text(itemJ.coordinate[0], itemJ.coordinate[1], itemJ.getID(),color='r', alpha=0.5)

plt.scatter(P1[0],P1[1],s=50,c="b")
plt.scatter(P2[0],P2[1],s=50,c="b")
plt.scatter(getmin_p1[1][0],getmin_p1[1][1],s=50,c='g')
plt.scatter(getmin_p2[1][0],getmin_p2[1][1],s=50,c='g')
endTime = datetime.datetime.now()
print('本次程序运行时间为：', endTime-startTime)
plt.show()