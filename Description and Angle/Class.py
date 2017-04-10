import pandas as pd
import numpy as np
import math

class Building:
    id = []
    description = []
    cordinations = []
    bezierP = []
    tempCount = 0

    def __init__(self, d, c):
        self.id = Building.tempCount + 1
        self.description = d
        self.cordinations = c
        Building.tempCount += 1
        
    def getID(self):
        return self.id

    def getDescription(self):
        return self.description

    def getCordinations(self):
        return self.cordinations

    def getBezier(self):
        return self.bezierP


class Road:
    id = []
    description = []
    cordinations = []
    bezierP = []
    tempCount = 0

    def __init__(self, d, c):
        self.id = Road.tempCount + 1
        self.description = d
        self.cordinations = c
        Road.tempCount += 1

    def insertCordination(self,minD_app,insert_c):
        if minD_app in self.cordinations:
            for i in range(len(self.cordinations)-1):
                if (minD_app[0] == self.cordinations[i]) & (minD_app[1] == self.cordinations[i+1]):
                    self.cordinations.insert(i+1,insert_c)
                else:return "区间不匹配"
        else:return "出错！所选区间不再Cordinations内"

    def divideByJointList(self, JointList):
        RoadList = []
        c = self.getCordinations()
        # p = self.getDescription()
        # endRoad = []
        tempI = []
        # count = 1
        tempRoad = []
        for i in c:  # 循环道路的坐标
            if (len(tempI) != 0) & (tempI not in tempRoad):
                tempRoad.append(tempI)
                tempI = []
            if i in JointList:
                tempRoad.append(i)
                if len(tempRoad) > 1:  # 子路段（原路段）的长度必须要大于1，否则抛弃。
                    RoadList.append(tempRoad)
                tempI = i
                # print("tempRoad:",tempRoad)
                # print("tempI:",tempI,"\n")
                tempRoad = []
            else:
                tempRoad.append(i)

        if len(tempRoad) != 0:  # 末尾坐标不是交叉点，还是要加入分段
            if len(tempRoad) > 1:
                RoadList.append(tempRoad)

        return RoadList

    def getMoreData(self, k):
        x_list = []
        y_list = []
        for i in np.arange(len(self.cordinations)):
            if i - 1 >= 0:
                x_diff = self.cordinations[i][0] - self.cordinations[i - 1][0]
                y_diff = self.cordinations[i][1] - self.cordinations[i - 1][1]
                for j in np.arange(k):
                    x_list.append(self.cordinations[i - 1][0] + x_diff * j / k)
                    y_list.append(self.cordinations[i - 1][1] + y_diff * j / k)
        list_final = list(zip(x_list, y_list))
        return list_final

    def getAngle(self):
         x_div = self.cordinations[0][0] - self.cordinations[-1][0]
         y_div = self.cordinations[0][1] - self.cordinations[-1][1]
         if x_div == 0:
            ang = 90
         elif y_div ==0:
            ang = 0
         else:
            ang = round(math.atan(y_div / x_div) * 180 / math.pi,2)
         return ang

    def getAnglelist(self):
        anglist = []
        for i in np.arange(len(self.cordinations)):
            if i - 1 >= 0:
                x_div = self.cordinations[i][0] - self.cordinations[i - 1][0]
                y_div = self.cordinations[i][1] - self.cordinations[i - 1][1]
                if (x_div == 0) & (y_div > 0):
                    ang = 0
                elif (x_div == 0) & (y_div < 0):
                    ang = 180
                elif (y_div == 0) & (x_div > 0):
                    ang = 90
                elif (y_div == 0) & (x_div < 0):
                    ang = 270
                elif (x_div > 0):
                    ang = 90 - math.atan(y_div / x_div) * 180 / math.pi
                elif (x_div < 0):
                    ang = 270 - math.atan(y_div / x_div) * 180 / math.pi
                anglist.append(ang)
        for i in range(len(anglist) - 1):
            if anglist[i + 1] - anglist[i] > 180:
                anglist[i + 1] = anglist[i + 1] - 360
            elif anglist[i + 1] - anglist[i] < -180:
                anglist[i + 1] = anglist[i + 1] + 360
        return anglist

    def getDistanceRate(self):
        distancelist = []
        dis = 0
        disratelist = []
        for i in range(len(self.cordinations)):
            if i - 1 >= 0:
                x_div = self.cordinations[i][0] - self.cordinations[i - 1][0]
                y_div = self.cordinations[i][1] - self.cordinations[i - 1][1]
                distance = np.sqrt(x_div**2 + y_div**2)
                distancelist.append(distance)
                dis = dis+distance
        for distan in distancelist:
            rate = distan/dis
            disratelist.append(rate)
        return disratelist,dis

    def getScore(self):
        ascore = 0
        angmean = np.mean(self.getAnglelist())
        angstd = np.std(self.getAnglelist())
        for j in range(len(self.getAnglelist())):
            score = (self.getDistanceRate()[0][j]*(self.getAnglelist()[j]- angmean))**2
            ascore = ascore+ score
        angscore = (ascore/len(self.getAnglelist()))**0.5
        return angmean,angstd,angscore

    def getMiddlePoint(self):
        p_x = list(zip(*self.cordinations))[0]
        p_y = list(zip(*self.cordinations))[1]
        x = sum(p_x)/len(self.cordinations)
        y = sum(p_y)/len(self.cordinations)
        list_mp = [x,y]
        return  list_mp
    def getMiddleCordination(self):
        lenc = len(self.cordinations)
        middlec = self.cordinations[round(lenc/2)]
        return middlec

    def getFilterAnglelist(self):
        k = 0
        filterAnglelist = []
        for i in np.arange(len(self.getAnglelist())):
            if i + 1 < len(self.getAnglelist()):
                a = self.getAnglelist()[i]
                b = self.getAnglelist()[i + 1]
                if (((a <= 0) & (b > 0)) | ((a > 0) & (b <= 0))):
                    temp = self.getAnglelist()[k:i + 1]
                    filterAnglelist.append(temp)
                    k = i + 1
                elif i + 1 == len(self.getAnglelist()) - 1:
                    filterAnglelist.append(self.getAnglelist()[k:i + 2])
        return filterAnglelist

    def getID(self):
        return self.id

    def getDescription(self):
        return self.description

    def getCordinations(self):
        return self.cordinations

    def getBezier(self):
        return self.bezierP

    def printRS(self):
        print("\n道路id： ", self.id, "\n道路描述： ", self.description, "\n道路坐标： ", self.cordinations, "\n贝塞尔描述： ",
              self.bezierP)

    def getCount(self):
        print('Count: %d' % Road.tempCount)
        return Road.tempCount

class TempRoad(Road):
    id = []
    description = []
    cordinations = []
    bezierP = []
    tempCount = 0

    def __init__(self, d, c):
        self.id = Road.tempCount + 1
        self.description = d
        self.cordinations = c
        Road.tempCount += 1
#根据描述划分的道路类
class SRoad(Road):
    sonroads = []
    sid = []
    sCount = 0

    def __init__(self, r ,c,son):
        """
        :type r: object
        """
        self.sonroads = son
        self.sid = SRoad.sCount + 1
        self.cordinations = c
        self.description = r.description
        SRoad.sCount += 1

    def divideByJointList(self, JointList):
        RoadList = []
        c = self.getAllCordinations()
        # p = self.getDescription()
        # endRoad = []
        tempI = []
        # count = 1
        tempRoad = []
        for i in c:  # 循环道路的坐标
            if (len(tempI) != 0) & (tempI not in tempRoad):
                tempRoad.append(tempI)
                tempI = []
            if i in JointList:
                tempRoad.append(i)
                if len(tempRoad) > 1:  # 子路段（原路段）的长度必须要大于1，否则抛弃。
                    RoadList.append(tempRoad)
                tempI = i
                # print("tempRoad:",tempRoad)
                # print("tempI:",tempI,"\n")
                tempRoad = []
            else:
                tempRoad.append(i)

        if len(tempRoad) != 0:  # 末尾坐标不是交叉点，还是要加入分段
            if len(tempRoad) > 1:
                RoadList.append(tempRoad)

        return RoadList

    def getMoreData(self, k):
        x_list = []
        y_list = []
        list_final = []
        for data in self.cordinations:
            for i in np.arange(len(data)):
                if i - 1 >= 0:
                    x_diff = data[i][0] - data[i - 1][0]
                    y_diff = data[i][1] - data[i - 1][1]
                    for j in np.arange(k):
                        x_list.append(data[i - 1][0] + x_diff * j / k)
                        y_list.append(data[i - 1][1] + y_diff * j / k)
            list_final.append(list(zip(x_list, y_list)))
        cor_list = []
        for data in list_final:
            for temp in data:
                cor_list.append(temp)
        return cor_list

    def setCordinations(self,data):
        list_c = []
        if data == None:
            list_c.append(self.cordinations)
            cordination = list_c
            self.cordinations = cordination
        else:
            list_ca = []
            for item in self.cordinations:
                list_ca.append(item)
            list_ca.append(data)
            self.cordinations = list_ca
# [[[],[],[]]]
    def getAllCordinations(self):
        corlist = []
        for data in self.cordinations:
            for temp in data:
                corlist.append(temp)
        return corlist

    def getID(self):
        return  self.sid

    def setSon(self, s):
        list_son = []
        list_son.append(self.sonroads)
        son_ = list_son
        if s == None:
            self.sonroads = son_
        else:
            list_s =[]
            for item in self.sonroads:
                list_s.append(item)
            list_s.append(s)
            self.sonroads = list_s

    def getSonRoads(self):
        return self.sonroads

#单线路与双行道道路类
class FRoad(SRoad):
    sonroads = []
    fid = []
    fCount = 0

    def __init__(self,r,c,son):
        self.sonroads = son
        self.fid = FRoad.fCount + 1
        self.cordinations = c
        self.description = r.description
        FRoad.fCount += 1


# 子路段数据结构
# 每个路段都有个id号     #description作为路段类型的描述     #cordinations 路段的采样坐标     #用bezierP拟合的采样点描述
class Segment:
    id = []
    belongRoadID = []
    description = []
    coordinations = []
    bezierP = []
    tempCount = 0
    Head = None
    Tail = None

    def __init__(self, bID, d, c):
        self.id = Segment.tempCount + 1
        # self.belongRoad = Road 其实可以嵌入Road类
        self.belongRoadID = bID
        self.description = d
        self.cordinations = c
        Segment.tempCount += 1

    def getMoreData(self, k):
        x_list = []
        y_list = []
        for i in np.arange(len(self.cordinations)):
            if i - 1 >= 0:
                x_diff = self.cordinations[i][0] - self.cordinations[i - 1][0]
                y_diff = self.cordinations[i][1] - self.cordinations[i - 1][1]
                for j in np.arange(k):
                    x_list.append(self.cordinations[i - 1][0] + x_diff * j / k)
                    y_list.append(self.cordinations[i - 1][1] + y_diff * j / k)
        list_final = list(zip(x_list, y_list))
        return list_final

    def getAnglelist(self):
        anglist = []
        for i in np.arange(len(self.cordinations)):
            if i - 1 >= 0:
                x_div = self.cordinations[i][0] - self.cordinations[i - 1][0]
                y_div = self.cordinations[i][1] - self.cordinations[i - 1][1]
                if (x_div == 0) & (y_div > 0):
                    ang = 0
                elif (x_div == 0) & (y_div < 0):
                    ang = 180
                elif (y_div == 0) & (x_div > 0):
                    ang = 90
                elif (y_div == 0) & (x_div < 0):
                    ang = 270
                elif (x_div > 0):
                    ang = 90 - math.atan(y_div / x_div) * 180 / math.pi
                elif (x_div < 0):
                    ang = 270 - math.atan(y_div / x_div) * 180 / math.pi
                anglist.append(ang)
        return anglist

    def getDistanceRate(self):
        distancelist = []
        dis = 0
        disratelist = []
        for i in range(len(self.cordinations)):
            if i - 1 >= 0:
                x_div = self.cordinations[i][0] - self.cordinations[i - 1][0]
                y_div = self.cordinations[i][1] - self.cordinations[i - 1][1]
                distance = np.sqrt(x_div**2 + y_div**2)
                distancelist.append(distance)
                dis = dis+distance
        for distan in distancelist:
            rate = distan/dis
            disratelist.append(rate)
        return disratelist,dis

    def getScore(self):
        ascore = 0
        angmean = np.mean(self.getAnglelist())
        angstd = np.std(self.getAnglelist())
        for j in range(len(self.getAnglelist())):
            score = (self.getDistanceRate()[0][j]*(self.getAnglelist()[j]- angmean))**2
            ascore = ascore+ score
        angscore = (ascore/len(self.getAnglelist()))**0.5
        return angmean,angstd,angscore

    def getMiddlePoint(self):
        p_x = list(zip(*self.cordinations))[0]
        p_y = list(zip(*self.cordinations))[1]
        x = sum(p_x)/len(self.cordinations)
        y = sum(p_y)/len(self.cordinations)
        list_mp = [x,y]
        return  list_mp

    def setHeadJoint(self, J):
        self.Head = J
        # return self.cordinations[0]

    def setTailJoint(self, J):
        self.Tail = J

    def getHead(self):
        return self.cordinations[0]

    def getTail(self):
        return self.cordinations[-1]

    def getLength(self):
        former = []
        LEN = 0
        for item in self.cordinations:
            if len(former) != 0:
                LEN = LEN + ((item[0] - former[0]) ** 2 + (item[1] - former[1]) ** 2) ** 0.5
                former = item
            else:
                former = item
        return LEN


    def getbID(self):
        return self.belongRoadID

    def getID(self):
        return self.id

    def getDescription(self):
        return self.description

    def getCordinations(self):
        return self.cordinations

    def printRS(self):
        print("\n道路id： ", self.id, "从属道路ID：", self.belongRoadID, "\n道路描述： ", self.description, "\n道路坐标： ",
              self.cordinations, "\n贝塞尔描述： ", self.bezierP)

    def getCount(self):
        print('Total Counts: %d' % Segment.tempCount)
        return Segment.tempCount

class FSegment(Segment):
    id = []
    belongRoadID = []
    description = []
    cordinations = []
    tempCount = 0
    Head = None
    Tail = None

    def __init__(self, bID, d, c):
        self.id = FSegment.tempCount + 1
        # self.belongRoad = Road 其实可以嵌入Road类
        self.belongRoadID = bID
        self.description = d
        self.cordinations = c
        FSegment.tempCount += 1

# Joint交叉点数据结构
class Joint:
    id = 0
    coordinate = []  # 交叉路口坐标
    neighborSegment = []  # 交叉路口连接的子路段

    # id = 0

    def __init__(self, coordinate):
        self.id = Joint.id + 1
        Joint.id += 1
        self.coordinate = coordinate
        self.neighborSegment = []

    def getCoordinate(self):
        return self.coordinate

    def getID(self):
        return self.id

    def isIDinNeighborSegment(self, ID):
        for item in self.neighborSegment:
            # print('self.neighborSegment len:',len(self.neighborSegment))
            if ID == item.id:
                # self.printJoint()
                # print('ID:',ID)
                # print('self.neighborSegment len:',len(self.neighborSegment))
                item.printRS()
                return item

    def getNeighborSegment(self):
        return self.neighborSegment

    def getNeighborJointID(self):
        tempList = []
        for item in self.neighborSegment:
            if item.getHead() == self.coordinate:
                if item.Tail is not None:
                    tempList.append(item.Tail.id)
            elif item.getTail() == self.coordinate:
                if item.Head is not None:
                    tempList.append(item.Head.id)
            else:
                print('警告，在邻居边Segment中未匹配出邻居Joint.ID！！！')
                print('self.coordinate:', self.coordinate)
                print('item.getHead():', item.getHead(), '\t', 'item.getTail():', item.getTail())
        return tempList

    def getNeighborEdge(self):
        tempList = []
        for item in self.neighborSegment:
            if item.getHead() == self.coordinate:
                if item.Tail is not None:
                    tempList.append([item.Tail.id, item.getLength()])
            elif item.getTail() == self.coordinate:
                if item.Head is not None:
                    tempList.append([item.Head.id, item.getLength()])
            else:
                print('警告，在邻居边Segment中未匹配出邻居Joint.ID！！！')
                print('self.coordinate:', self.coordinate)
                print('item.getHead():', item.getHead(), '\t', 'item.getTail():', item.getTail())
        return tempList

    def appendNeighborSegment(self, r):
        self.neighborSegment.append(r)

    def printJoint(self):
        print("\n交叉点坐标为：", self.coordinate, "\n交叉点连接的路网个数为：", len(self.neighborSegment))

# 每一次计算要建立新的tJoint
class tJoint(Joint):
    parent = None
    g = float('inf')
    f = float('inf')

    def __init__(self, j):
        self.id = j.id
        self.coordinate = j.coordinate
        self.neighborSegment = j.neighborSegment

    def set_g(self, g1):
        self.g = g1

    def set_f(self, f1):
        self.f = f1

    def set_parent(self, p):
        self.parent = p
