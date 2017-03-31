from getdata import *
from Class import *
import pickle
import pandas as pd
from theFunctions import *

jsonURL = 'street2.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList,crossList)
froadList = GetData.getFRoadlist(roadList,0.0025,25)
fcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[0]
fsegmentList = GetData.getFsegmentlist(roadList,0.0025,25)
fjointList = GetData.getJointlist(fsegmentList, fcrosslist)

print (fjointList[0].getID())
def findJointByCoordinate(C, jointList):  # 通过交叉点的坐标找出交叉点的ID
    for item in jointList:
        if item.coordinate == C:
            return item

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