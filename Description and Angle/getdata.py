# -*- coding: utf-8 -*-
import Class as RoadClass
import pandas as pd
import re
from theFunctions import *

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

    def getFCrosslist(roadlist,dis,divang):
        froadlist = GetData.getFRoadlist(roadlist,dis,divang)
        fcList = []
        fnlist = []
        tempRoadList = []
        crossList = GetData.getCrosslist(roadlist)
        for data in froadlist:
            if len(data.getCordinations()) ==2:
                for cdata in crossList:
                    # if cdata in data.getSonRoads()[0].getCordinations():
                    #     # tr = RoadClass.TempRoad(data.getSonRoads()[0].description, data.getSonRoads()[0].cordinations)
                    #     # tempRoadList.append(tr)
                    #     point = get_mindisandcordinations(data.getSonRoads()[1], cdata)[1]
                    #     minD_app = get_mindisandcordinations(data.getSonRoads()[1], cdata)[2]
                    #     # tr2 = RoadClass.TempRoad(data.getSonRoads()[1].description, data.getSonRoads()[1].cordinations)
                    #     # tr2.insertCordination(minD_app,point)
                    #     # tempRoadList.append(tr2)
                    #     fnlist.append(point)
                    #     fcList.append([point,cdata])
                    #
                    # elif cdata in data.getSonRoads()[1].getCordinations():
                    #     point = get_mindisandcordinations(data.getSonRoads()[0], cdata)[1]
                    #     minD_app = get_mindisandcordinations(data.getSonRoads()[0], cdata)[2]
                    #     # data.getSonRoads()[1].insertCordination(minD_app, point)
                    #     fnlist.append(point)
                    #     fcList.append([point, cdata])
                    if cdata in data.getCordinations()[0]:
                        cor = data.getCordinations()[1]
                        min = ((cor[0][0] - cdata[0]) ** 2 + (cor[0][1] - cdata[1]) ** 2) ** 0.5
                        point = cor[0]
                        for i in range(len(cor)):
                            dis = ((cor[i][0] - cdata[0]) ** 2 + (cor[i][1] - cdata[1]) ** 2) ** 0.5
                            if dis < min:
                                min = dis
                                point = cor[i]
                        fnlist.append(point)
                        fcList.append([point,cdata])
                    elif cdata in data.getCordinations()[1]:
                        cor = data.getCordinations()[0]
                        min = ((cor[0][0] - cdata[0]) ** 2 + (cor[0][1] - cdata[1]) ** 2) ** 0.5
                        point = cor[0]
                        for i in range(len(cor)):
                            dis = ((cor[i][0] - cdata[0]) ** 2 + (cor[i][1] - cdata[1]) ** 2) ** 0.5
                            if dis < min:
                                min = dis
                                point = cor[i]
                        fnlist.append(point)
                        fcList.append([point,cdata])
                    else:
                        pass
                        # 交叉点会有重复的，去重。set好像不支持二维列表。
            # else:
            #     tr = RoadClass.TempRoad(data.description,data.cordinations[0])
            #     tempRoadList.append(tr)

        notrealcrosslist_1 = []
        for nd in fnlist:
            if nd not in notrealcrosslist_1:
                notrealcrosslist_1.append(nd)
        notrealdouble = []
        for nrd in fcList:
            if nrd not in notrealdouble:
                notrealdouble.append(nrd)

        for cc in crossList:
            fnlist.append(cc)
        fcrosslist = []
        for item in fnlist:
            if item not in fcrosslist:
                fcrosslist.append(item)
        notrealcrosslist = [j for j in notrealcrosslist_1 if j not in crossList]
        notrealdoublelist = [k for k in notrealdouble if k[0] not in crossList]

        return fcrosslist,notrealcrosslist,notrealdoublelist

    def getCrosslist(roadlist):
        # 获得路网的交叉点（路A与路B的坐标相同的点判定为相交点。）
        ccList = []
        for item in roadlist:
            ccList.append(item.getCordinations())
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
                if itemC in itemR.cordinations:
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

    def getFsegmentlist(roadlist,dis,divang):
        fcrosslist = GetData.getFCrosslist(roadlist,dis,divang)[0]
        # 取数据中带有交叉点的路
        for itemC in fcrosslist:
            list1 = []
            for itemR in roadlist:
                if itemC in itemR.cordinations:
                    list1.append(itemR)

        fsegmentlist = []
        count = 0
        for item in roadlist:
            tempList1 = item.divideByJointList(fcrosslist)
            if GetData.isContinuous(tempList1) is not True:
                print("警告，道路划分后，不连续！！！！")
                # print (len(roadList1))
            for segmentCordination in tempList1:
                count += 1
                fsegmentlist.append(RoadClass.FSegment(item.id, item.description, segmentCordination))
        othercrossinfo = GetData.getFCrosslist(roadlist,dis,divang)[2]
        for item2 in othercrossinfo:
            fsegmentlist.append(RoadClass.FSegment(None, None, item2))
        return fsegmentlist

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
                    if len(jointC.neighborSegment) >= 2:
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
            if 'bridge' not in data.getDescription():
                if 'name' in data.getDescription():
                    if data.getDescription()['name'] not in deslist:
                        sroad = RoadClass.SRoad(data,data.getCordinations(),data)
                        sroad.setCordinations(None)
                        sroad.setSon(None)
                        deslist.append(data.getDescription()['name'])
                        sroadlist.append(sroad)
                    else:
                        for item in sroadlist:
                            if 'name' in item.getDescription():
                                if item.getDescription()['name'] == data.getDescription()['name']:
                                    item.setCordinations(data.getCordinations())
                                    item.setSon(data)
                else:
                    sroad = RoadClass.SRoad(data,data.getCordinations(),data)
                    sroad.setCordinations(None)
                    sroad.setSon(None)
                    sroadlist.append(sroad)
        return  sroadlist

    def filterlist(sameroadlist, l):
        md_finnal = []
        md_list = []
        for rl in sameroadlist:
            md_list.append(rl.getMiddlePoint())

        for i in range(len(md_list)):
            l_a = []
            l_b = []
            for j in range(len(md_list)):
                if i < j:
                    dis = ((md_list[i][0] - md_list[j][0]) ** 2 + (md_list[i][1] - md_list[j][1]) ** 2) ** 0.5
                    if dis < l:
                        l_a.append(sameroadlist[i])
                        l_a.append(sameroadlist[j])
                        l_a.append(dis)
                        if l_a != []:
                            l_b.append(l_a)
                            l_a = []
            mindis = l
            if l_b != []:
                for m in range(len(l_b)):
                    if l_b[m][2] < mindis:
                        mindis = l_b[m][2]
                        l_amin = l_b[m]
                md_finnal.append(l_amin)
        md_fin = []
        for mdd in md_finnal:
            if mdd not in md_fin:
                md_fin.append(mdd)
        md_fin2 = md_fin
        for imd in md_fin:
            for jmd in md_fin:
                if (imd[0] == jmd[1]) | (imd[1] == jmd[0]):
                    if imd[2] < jmd[2]:
                        md_fin2.remove(jmd)
                    elif imd in md_fin2:
                        md_fin2.remove(imd)
        md_fin = md_fin2
        return md_fin

    def getFRealteddata(roadlist,dis,divang):
        s = GetData.getParallelroadIDList(roadlist)
        fl = GetData.filterlist(s, dis)
        dissameroadlist = []
        for i in range(len(fl)):
            list_i = fl[i][0:2]
            dissameroadlist.append(list_i)
        angelesameroadlist = []
        for road_data in dissameroadlist:
            if (road_data[0].getScore()[0] - divang < road_data[1].getScore()[0] < road_data[0].getScore()[
                0] + divang) | \
                    (road_data[0].getScore()[0] - divang < road_data[1].getScore()[0] - 180 < road_data[0].getScore()[
                        0] + divang) | \
                    (road_data[0].getScore()[0] - divang < road_data[1].getScore()[0] + 180 < road_data[0].getScore()[
                        0] + divang):
                angelesameroadlist.append(road_data)
        finnal_list = GetData.tolist(angelesameroadlist)
        list_out = [i for i in s if i not in finnal_list]

        return angelesameroadlist,list_out

    def getFRoadlist(roadlist,dis,divang):
        froadlist = []
        sroadList = GetData.getSRoadlist(roadlist)
        #将非Des相同划分为FRoad
        for a in sroadList:
            if len(a.getSonRoads()) == 1:
                froad = RoadClass.FRoad(a.getSonRoads()[0],a.getSonRoads()[0].getCordinations(),a.getSonRoads()[0])
                froad.setCordinations(None)
                froad.setSon(None)
                froadlist.append(froad)
        doubleroadlist = GetData.getFRealteddata(roadlist,dis,divang)[0]
        onewaylist = GetData.getFRealteddata(roadlist,dis,divang)[1]
        # 将划分出的单行道划分为FRoad
        for b in onewaylist:
            froad1 = RoadClass.FRoad(b,b.getCordinations(),b)
            froad1.setCordinations(None)
            froad1.setSon(None)
            froadlist.append(froad1)
        # 将划分出的双行道划分为FRoad
        for c in doubleroadlist:
            froad2 = RoadClass.FRoad(c[0],c[0].getCordinations(),c[0])
            froad2.setCordinations(None)
            froad2.setSon(None)
            froad2.setCordinations(c[1].getCordinations())
            froad2.setSon(c[1])
            froadlist.append(froad2)

        return  froadlist


    def getBridgelist(roadlist):
        bridgelist = []
        for data in roadlist:
            if 'bridge' in data.getDescription():
                if data.getDescription()['bridge'] == 'yes':
                    bridgelist.append(data)
        return bridgelist


    def tolist(list):
        list_one = []
        for i in list:
            for j in i:
                list_one.append(j)
        return list_one

    def getParallelroadIDList(roadList):
        sroadList = GetData.getSRoadlist(roadList)
        sroadIDList = []
        sl = []
        for a in sroadList:
            if len(a.getSonRoads()) >= 2:
                sl.append(a.getSonRoads())
        sroadIDList = GetData.tolist(sl)
        return sroadIDList


if __name__ == "__main__":
    roadname = "金田路"
    jsonURL = 'C:\\Users\\Cimucy\\Documents\\Python Scripts\\毕业设计\\street2.json'
    jsondata = pd.read_json(jsonURL)
    roadList = GetData.getRoadlist(jsondata)
    sroadList = GetData.getSRoadlist(roadList)
    crossList = GetData.getCrosslist(sroadList)
    segmentList = GetData.getsegmentlist(roadList, crossList)
    jointList = GetData.getJointlist(segmentList, crossList)
    NeighborSegment = GetData.getNeighborSegment(segmentList, [114.0378885, 22.5589664])
    jtroad = GetData.searchroad(jsondata, roadname)

    print('路网条数有：', len(roadList))
    print('道路条数有：',len(sroadList))
    print('交叉点个数：', len(crossList))
    print('子路段个数为：', len(segmentList))
    print('Joint点长度为：', len(jointList))
    print('交叉点子路段：', NeighborSegment)
    print('%s采样路段个数:' % roadname, jtroad[0])
    import matplotlib.pyplot as plt

    sl = []
    for a in sroadList:
        s = a.getSonRoads()
        if len(s)>=2:
            print (s)
            sl.append(s)
    print (sl)

    sl_l = []
    for sl_1 in sl:
        for sl_2 in sl_1:
            sl_l.append(sl_2)
    print(sl_l)

    print(GetData.tolist(sl))
    for data in sroadList[4:5]:
        son = data.getSonRoads()
        id = data.getID()
        print (id)
        sid = data.getCordinations()
        x = []
        y = []
        x1= []
        y1 = []
        print (sid)
        if len(sid) == 2:
            for temp in sid[0]:
                X = temp[0]
                Y = temp[1]
                x.append(X)
                y.append(Y)
            plt.plot(x,y,'r')
            for temp in sid[1]:
                X1 = temp[0]
                Y1 = temp[1]
                x1.append(X1)
                y1.append(Y1)
            plt.plot(x1,y1,'b')
        else:
            for temp in sid[0]:
                X = temp[0]
                Y = temp[1]
                x.append(X)
                y.append(Y)
            plt.plot(x,y,'r')
    plt.show()

