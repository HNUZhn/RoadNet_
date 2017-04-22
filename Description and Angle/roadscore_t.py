# -*- coding: utf-8 -*-
import Class as RoadClass
import pandas as pd
import re
import numpy as np

class GetData:
    def getRoadlist(data):
        roadnetworkType = ['primary_link', 'secondary_link', 'tertiary_link', 'primary', 'secondary', 'trunk_link',
                           'service', 'tertiary', 'trunk', 'residential', 'unclassified']
        ##路网信息文件结构分析分析
        roadList = []
        # crossList = []
        for item in data.features:
            if len(item['geometry']) > 0:  # 保证有数据
                if item['geometry']['type'] == 'LineString':  # 保证是直线类型
                    if 'highway' in item['properties']:  # 是highway类型
                        if item['properties']['highway'] in roadnetworkType:  # 在预设规定的类型中
                            roadList.append(RoadClass.Road(item['properties'], item['geometry']['coordinates']))
        return roadList

    def getCrosslist(sroadlist):
        # 获得路网的交叉点（路A与路B的坐标相同的点判定为相交点。）
        ccList = []
        for item in sroadlist:
            ccList.append(item.getAllCordinations())
        cc = []
        for i in ccList:
            for j in ccList:
                if i != j:  # 找两条不同的路网比较
                    for ii in i:
                        for jj in j:
                            if ii == jj:
                                cc.append(ii)

        # 交叉点会有重复的，去重。set好像不支持二维列表。
        crosslist = []
        for item in cc:
            if item not in crosslist:
                crosslist.append(item)
        return crosslist

    def isContinuous(List):  # 判断道路是否连续
        tempH = []
        if len(tempH) != 0:
            for item in List:
                if tempH[-1] == item[0]:
                    # 判断两组数据第一个点与最后一点是否相同来判断是否连续
                    tempH = item
                else:
                    return False
        return True

    def getsegmentlist(roadlist, crosslist):
        # 取数据中带有交叉点的路
        for itemC in crosslist:
            list1 = []
            for itemR in roadlist:
                if itemC in itemR.getCordinations():
                    list1.append(itemR)

        segmentlist = []
        count = 0
        for item in roadlist:
            tempList1 = item.divideByJointList(crosslist)
            if GetData.isContinuous(tempList1) is not True:
                print("警告，道路划分后，不连续！！！！")
                # print (len(roadList1))
            for segmentCordination in tempList1:
                count += 1
                segmentlist.append(RoadClass.Segment(item.id, item.description, segmentCordination))
        return segmentlist

    def getSroadsegmentist(sroadlist,crosslist):
        # 取数据中带有交叉点的路
        for itemC in crosslist:
            list1 = []
            for itemR in sroadlist:
                if itemC in itemR.getAllCordinations():
                    list1.append(itemR)

        ssegmentlist = []
        count = 0
        for item in sroadlist:
            templist = []
            if len(item.getCordinations()) == 1:
                for data in item.divideByJointList(crosslist):
                    templist.append(data)
            else:
                tempI = []
                tempO = []
                tempRoad = []
                tempRoad2 = []
                othertempRoad = []
                for t in [0,1]:
                    a = [0,1]
                    if t == 0:
                        m = 1
                    else:
                        m = 0
                    for k in np.arange(min(len(item.getCordinations()[t]),len(item.getCordinations()[m]))):
                        i = item.getCordinations()[t][k]
                        j = item.getCordinations()[m][k]
                        if (len(tempI) != 0) & (tempI not in tempRoad):
                            tempRoad.append(tempI)
                            tempRoad2.append(tempO)
                            tempI = []
                            tempO = []
                        if i in crosslist:
                            tempRoad.append(i)
                            tempRoad2.append(j)
                            if len(tempRoad) > 1:  # 子路段（原路段）的长度必须要大于1，否则抛弃。
                                templist.append(tempRoad)
                                templist.append(tempRoad2)
                            tempI = i
                            tempO = j
                            tempRoad = []
                            tempRoad2 = []
                        else:
                            tempRoad.append(i)
                            othertempRoad.append(j)

                if len(tempRoad) != 0:  # 末尾坐标不是交叉点，还是要加入分段
                    if len(tempRoad) > 1:
                        templist.append(tempRoad)
                if len(othertempRoad) != 0:  # 末尾坐标不是交叉点，还是要加入分段
                    if len(othertempRoad) > 1:
                        templist.append(othertempRoad)
            templist_f = []
            for data_f in templist:
                if data_f not in templist_f:
                    templist_f.append(data_f)

            if GetData.isContinuous(templist_f) is not True:
                print("警告，道路划分后，不连续！！！！")
                # print (len(roadList1))
            for segmentCordination in templist_f:
                count += 1
                ssegmentlist.append(RoadClass.Segment(item.id, item.description, segmentCordination))
        return ssegmentlist

    def getSamesegment(segmentID,roadlist):
        samesegment = []
        sroadlist = GetData.getSRoadlist(roadlist)
        crosslist = GetData.getCrosslist(sroadlist)
        segmentlist = GetData.getsegmentlist(roadlist,crosslist)
        for data in segmentlist:
            if data.getID() == segmentID:
                rbID = data.getbID()
                cor = data.getCordinations()
                corlist = []
                rblist = []
                for item in sroadlist:
                    son = item.getSonRoads()
                    if len(son) == 1:
                        return "该子路段无同名对应子路段"
                    elif rbID in son:
                        for roadid in son:
                            for rd in roadlist:
                                if rd.getID() == roadid:
                                    if rd.getID() == rbID:
                                        rblist.append(rd.getCordinations())
                                    else:
                                        bid = rd.getID()
                                        corlist.append(rd.getCordinations())
                                head = rblist.index(data.getHead())
                                tail = rblist.index(data.getTail())
                                samcor = corlist[head:tail]
                                samesegment.append(RoadClass.Segment(bid, data.description, samcor))
        return samesegment


    def getJointlist(segmentlist, crosslist):
        jointlist_1 = []
        for itemC in crosslist:
            # print(itemC)
            jointC = RoadClass.Joint(itemC)
            # print (jointC)
            for itemS in segmentlist:
                if (itemC in itemS.cordinations):
                    if not ((itemC == itemS.getHead()) | (itemC == itemS.getTail())):
                        print("\n\n警告，出现未划分的情况！！！！")
                if (itemC == itemS.getHead()) | (itemC == itemS.getTail()):
                    # if (itemC is itemS.getHead())|(itemC is itemS.getTail()):  #之前用is来判断，不对，隐藏的bug过了好久才发现。
                    jointC.appendNeighborSegment(itemS)
                    # 如果交叉点的邻居大于2（连接的子路段个数大于2），为交叉路口。
                    if len(jointC.neighborSegment) > 2:
                        jointlist_1.append(jointC)
        jointlist = []
        for clist in jointlist_1:
            if clist not in jointlist:
                jointlist.append(clist)
        return jointlist

    def getNeighborSegment(segmentlist, crossdata):
        neighborSegmentList = []
        jointC = RoadClass.Joint(crossdata)
        # print (jointC)
        for item in segmentlist:
            if (crossdata in item.cordinations):
                if not ((crossdata == item.getHead()) | (crossdata == item.getTail())):
                    print("\n\n警告，该点不是交叉！！！！")
                if (crossdata == item.getHead()) | (crossdata == item.getTail()):
                    # if (itemC is itemS.getHead())|(itemC is itemS.getTail()):  #之前用is来判断，不对，隐藏的bug过了好久才发现。
                    jointC.appendNeighborSegment(item)
                    # 如果交叉点的邻居大于2（连接的子路段个数大于2），为交叉路口。
                    if len(jointC.neighborSegment) >= 2:
                        for data in jointC.getNeighborSegment():
                            neighborSegmentList.append(data.getID())
        n = []
        for data in neighborSegmentList:
            if data not in n:
                n.append(data)
        neighborSegmentList = n
        return neighborSegmentList

    def searchroad(jsondata, roadname):
        roadnetworkType = ['primary_link', 'secondary_link', 'tertiary_link', 'primary', 'secondary', 'trunk_link',
                           'service', 'tertiary', 'trunk', 'residential', 'unclassified']
        locationdata = []
        for data in jsondata.features:
            if len(data['geometry']) > 0:
                if data['geometry']['type'] == 'LineString':  # 保证是直线类型
                    if 'name' in data['properties']:
                        if 'highway' in data['properties']:  # 是highway类型
                            if data['properties']['highway'] in roadnetworkType:
                                if re.match(roadname, data['properties']['name']) != None:
                                    locationdata.append(data["geometry"]["coordinates"])
        if len(locationdata) == 0:
            print("不存在%s" % roadname)
        return locationdata
    def getSRoadlist(roadlist):
        deslist = []
        sroadlist = []
        for data in roadlist:
            if 'name' in data.getDescription():
                if data.getDescription() not in deslist:
                    sroad = RoadClass.SRoad(data,data.getCordinations(),data.getID())
                    sroad.setCordinations(None)
                    sroad.setSon(None)
                    deslist.append(data.getDescription())
                    sroadlist.append(sroad)
                else:
                    for item in sroadlist:
                        if item.getDescription() == data.getDescription():
                            item.setCordinations(data.getCordinations())
                            item.setSon(data.getID())
            else:
                sroad = RoadClass.SRoad(data,data.getCordinations(),data.getID())
                sroad.setCordinations(None)
                sroad.setSon(None)
                sroadlist.append(sroad)
        return  sroadlist

    # def getParentRoad(sroadid):
    def getFrechetDistance(self,road1,road2):
        c1 = road1.getCordinations()
        c2 = road2.getCordinations()
        if (c1.getScore()[0]<45) |  (135<=c1.getScore()[0]<225) | (315<=c1.getScore()[0]):
            if ((c1[0][1] - c1[-1][1] > 0) & (c2[0][1] - c2[-1][1] < 0)) |  ((c1[0][1] - c1[-1][1] < 0) & (c2[0][1] - c1[-1][1] > 0)):
                c2_ = c2[::-1]
                for i in range(min(len(c1),len(c2_))):
                    max = 0
                    dis = ((c1[i][0]-c2_[i][0])**2+(c1[i][1]-c2_[i][1])**2)**0.5
                    if dis > max:
                        max = dis
            else:
                for i in range(min(len(c1),len(c2))):
                    max = 0
                    dis = ((c1[i][0]-c2[i][0])**2+(c1[i][1]-c2[i][1])**2)**0.5
                    if dis > max:
                        max = dis
        else:
            if ((c1[0][0] - c1[-1][0] > 0) & (c2[0][0] - c2[-1][0] < 0)) |  ((c1[0][0] - c1[-1][0] < 0) & (c2[0][0] - c1[-1][0] > 0)):
                c2_ = c2[::-1]
                for i in range(min(len(c1),len(c2_))):
                    max = 0
                    dis = ((c1[i][0]-c2_[i][0])**2+(c1[i][1]-c2_[i][1])**2)**0.5
                    if dis > max:
                        max = dis
            else:
                for i in range(min(len(c1),len(c2))):
                    max = 0
                    dis = ((c1[i][0]-c2[i][0])**2+(c1[i][1]-c2[i][1])**2)**0.5
                    if dis > max:
                        max = dis
        return  max

if __name__ == "__main__":
    roadname = "金田路"
    jsonURL = 'C:\\Users\\Cimucy\\Documents\\Python Scripts\\毕业设计\\street2.json'
    jsondata = pd.read_json(jsonURL)
    roadList = GetData.getRoadlist(jsondata)
    sroadList = GetData.getSRoadlist(roadList)
    crossList = GetData.getCrosslist(sroadList)
    segmentList = GetData.getsegmentlist(roadList, crossList)
    ssegmentList = GetData.getSroadsegmentist(sroadList,crossList)
    jointList = GetData.getJointlist(segmentList, crossList)
    NeighborSegment = GetData.getNeighborSegment(segmentList, [114.0378885, 22.5589664])
    jtroad = GetData.searchroad(jsondata, roadname)

    print('路网条数有：', len(roadList))
    print('道路条数有：',len(sroadList))
    print('交叉点个数：', len(crossList))
    print('子路段个数为：', len(segmentList))
    print('同路子路段个数为：', len(ssegmentList))
    print('Joint点长度为：', len(jointList))
    print('交叉点子路段：', NeighborSegment)
    print('%s采样路段个数:' % roadname, jtroad[0])
    # i= 0
    # for data in segmentList:
    #     print('子路段%s的均值标准差分数'%data.getID(), data.getScore())
    #     if data.getScore()[1]>10:
    #         i +=1
    # rate = round(i/len(segmentList),2)
    # print ("大于10的比例：",rate)
    # import matplotlib.pyplot as plt
    #
    # plt.figure()
    # for c in segmentList:
    #     if c.getID() == 1252:
    #         plt.subplot(2, 2, 1)
    #         print (c.getScore()[2],c.getDistanceRate()[1])
    #         std = c.getScore()[1]
    #         score= c.getScore()[2]
    #         a = u'std:%s score:%s'% (std,score)
    #         LonX = list(zip(*c.cordinations))[0]
    #         LatY = list(zip(*c.cordinations))[1]
    #         l1 = plt.plot(LonX, LatY, 'r',label =a )
    #         plt.xlim()
    #         plt.axis('equal')
    #         plt.xlabel(r'${Lon} $', fontsize=16)
    #         plt.ylabel(r'${Lat} $', fontsize=16)
    #         plt.legend(loc = 'best')
    #     if c.getID() == 1191:
    #         plt.subplot(2, 2, 2)
    #         print (c.getScore()[2],c.getDistanceRate()[1])
    #         std = c.getScore()[1]
    #         score= c.getScore()[2]
    #         a = u'std:%s score:%s'% (std,score)
    #         LonX = list(zip(*c.cordinations))[0]
    #         LatY = list(zip(*c.cordinations))[1]
    #         l2 = plt.plot(LonX, LatY, 'b',label = a)
    #         plt.xlim()
    #         plt.axis('equal')
    #         plt.xlabel(r'${Lon} $', fontsize=16)
    #         plt.ylabel(r'${Lat} $', fontsize=16)
    #         plt.legend(loc = 'best')
    #     if c.getID() == 1223:
    #         plt.subplot(2, 2, 3)
    #         print (c.getScore()[2],c.getDistanceRate()[1])
    #         std = c.getScore()[1]
    #         score= c.getScore()[2]
    #         a = u'std:%s score:%s'% (std,score)
    #         LonX = list(zip(*c.cordinations))[0]
    #         LatY = list(zip(*c.cordinations))[1]
    #         l3 = plt.plot(LonX, LatY, 'y',label = a)
    #         plt.xlim()
    #         plt.axis('equal')
    #         plt.xlabel(r'${Lon} $', fontsize=16)
    #         plt.ylabel(r'${Lat} $', fontsize=16)
    #         plt.legend(loc = 'best')
    #     if c.getID() == 1034:
    #         plt.subplot(2, 2, 4)
    #         print (c.getScore()[2],c.getDistanceRate()[1])
    #         std = c.getScore()[1]
    #         score= c.getScore()[2]
    #         a = u'std:%s score:%s'% (std,score)
    #         LonX = list(zip(*c.cordinations))[0]
    #         LatY = list(zip(*c.cordinations))[1]
    #         l4 = plt.plot(LonX, LatY, 'g',label = a)
    #         plt.xlim()
    #         plt.axis('equal')
    #         plt.xlabel(r'${Lon} $', fontsize=16)
    #         plt.ylabel(r'${Lat} $', fontsize=16)
    #         plt.legend(loc = 'best')
    #
    # equalseglist_l = []
    # for seg_data in segmentList:
    #     sameroadlist = []
    #     same_list = []
    #     for seg_data2 in segmentList:
    #         if seg_data.getID() != seg_data2.getID():
    #             if seg_data.getScore()[0] -5 < seg_data2.getScore()[0] <  seg_data.getScore()[0] +5:
    #                 if seg_data.getScore()[1] -5 < seg_data2.getScore()[1] <  seg_data.getScore()[1] +5:
    #                     if seg_data.getScore()[2] -3 < seg_data2.getScore()[2] <  seg_data.getScore()[2] + 3:
    #                         if seg_data.getDistanceRate()[1]-0.0001 < seg_data2.getDistanceRate()[1] < seg_data.getDistanceRate()[1]+0.0001:
    #                             same_list.append(seg_data.getID())
    #                             same_list.append(seg_data2.getID())
    #     for edata in same_list:
    #         if edata not in sameroadlist:
    #             sameroadlist.append(edata)
    #
    #     equalseglist_l.append(sameroadlist)
    # equalseglist = []
    # for edata in equalseglist_l:
    #     if edata not in equalseglist:
    #         equalseglist.append(edata)
    # print (equalseglist)
    # plt.show()

    i = 0
    for data in roadList:
        print('路段%s的均值标准差分数' % data.getID(), data.getScore())
        if data.getScore()[1] > 10:
            i += 1
    rate = round(i / len(roadList), 2)
    print("大于10的比例：", rate)
    import matplotlib.pyplot as plt

    plt.figure()
    for item in segmentList:
        LonX = list(zip(*item.cordinations))[0]
        LatY = list(zip(*item.cordinations))[1]
        plt.plot(LonX, LatY, c='k', linestyle='-', linewidth=2, alpha=0.5)
    for c in roadList:
        if c.getID() == 5:
            print(c.getScore()[2], c.getDistanceRate()[1])
            std = round(c.getScore()[1], 2)
            score = round(c.getScore()[2], 2)
            a = u'std:%s score:%s' % (std, score)
            LonX = list(zip(*c.cordinations))[0]
            LatY = list(zip(*c.cordinations))[1]
            l1 = plt.plot(LonX, LatY, 'r', linewidth=4, label=a)
        if c.getID() == 176:
            print(c.getScore()[2], c.getDistanceRate()[1])
            std = round(c.getScore()[1], 2)
            score = round(c.getScore()[2], 2)
            a = u'std:%s score:%s' % (std, score)
            LonX = list(zip(*c.cordinations))[0]
            LatY = list(zip(*c.cordinations))[1]
            l1 = plt.plot(LonX, LatY, 'b', linewidth=4, label=a)
            plt.xlim()
            plt.axis('equal')
            plt.xlabel(r'${Lon} $', fontsize=16)
            plt.ylabel(r'${Lat} $', fontsize=16)
            plt.legend()

    plt.figure()
    for c in roadList:
        if c.getID() == 490:
            plt.subplot(2, 2, 1)
            for item in segmentList:
                LonX = list(zip(*item.cordinations))[0]
                LatY = list(zip(*item.cordinations))[1]
                plt.plot(LonX, LatY, c='k', linestyle='-', linewidth=2, alpha=0.5)
            print(c.getScore()[2], c.getDistanceRate()[1])
            std = round(c.getScore()[1],2)
            score = round(c.getScore()[2],2)
            a = u'std:%s score:%s' % (std, score)
            LonX = list(zip(*c.cordinations))[0]
            LatY = list(zip(*c.cordinations))[1]
            l1 = plt.plot(LonX, LatY, 'r', linewidth=4,label=a)
            plt.xlim()
            plt.axis('equal')
            plt.xlabel(r'${Lon} $', fontsize=16)
            plt.ylabel(r'${Lat} $', fontsize=16)
            plt.legend()
        if c.getID() == 446:
            plt.subplot(2, 2, 2)
            for item in segmentList:
                LonX = list(zip(*item.cordinations))[0]
                LatY = list(zip(*item.cordinations))[1]
                plt.plot(LonX, LatY, c='k', linestyle='-', linewidth=2, alpha=0.5)
            print(c.getScore()[2], c.getDistanceRate()[1])
            std = round(c.getScore()[1],2)
            score = round(c.getScore()[2],2)
            a = u'std:%s score:%s' % (std, score)
            LonX = list(zip(*c.cordinations))[0]
            LatY = list(zip(*c.cordinations))[1]
            l2 = plt.plot(LonX, LatY, 'b',linewidth=4, label=a)
            plt.xlim()
            plt.axis('equal')
            plt.xlabel(r'${Lon} $', fontsize=16)
            plt.ylabel(r'${Lat} $', fontsize=16)
            plt.legend()
        if c.getID() == 223:
            plt.subplot(2, 2, 3)
            for item in segmentList:
                LonX = list(zip(*item.cordinations))[0]
                LatY = list(zip(*item.cordinations))[1]
                plt.plot(LonX, LatY, c='k', linestyle='-', linewidth=2, alpha=0.5)
            print(c.getScore()[2], c.getDistanceRate()[1])
            std = round(c.getScore()[1],2)
            score = round(c.getScore()[2],2)
            a = u'std:%s score:%s' % (std, score)
            LonX = list(zip(*c.cordinations))[0]
            LatY = list(zip(*c.cordinations))[1]
            l3 = plt.plot(LonX, LatY, 'y',linewidth=4, label=a)
            plt.xlim()
            plt.axis('equal')
            plt.xlabel(r'${Lon} $', fontsize=16)
            plt.ylabel(r'${Lat} $', fontsize=16)
            plt.legend()
        if c.getID() == 227:
            plt.subplot(2, 2, 4)
            for item in segmentList:
                LonX = list(zip(*item.cordinations))[0]
                LatY = list(zip(*item.cordinations))[1]
                plt.plot(LonX, LatY, c='k', linestyle='-', linewidth=2, alpha=0.5)
            print(c.getScore()[2], c.getDistanceRate()[1])
            std = round(c.getScore()[1],2)
            score = round(c.getScore()[2],2)
            a = u'std:%s score:%s' % (std, score)
            LonX = list(zip(*c.cordinations))[0]
            LatY = list(zip(*c.cordinations))[1]
            l4 = plt.plot(LonX, LatY, 'g',linewidth=4, label=a)
            plt.xlim()
            plt.axis('equal')
            plt.xlabel(r'${Lon} $', fontsize=16)
            plt.ylabel(r'${Lat} $', fontsize=16)
            plt.legend()

    plt.show()