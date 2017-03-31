import math
from readdata import *
from theFunctions import *
from Class import *
import pandas as pd
# from trajectory_filter_1 import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt ##　　% matplotlib qt5
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import datetime
startTime = datetime.datetime.now()
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

pf = pd.read_csv('street_SZ.csv')


def matchGPStoRoad(data,fsegmentlist,froadlist,angle):
    obxy = data.loc[:, ["Lon", "Lat", "Direct"]]
    dislist = []
    fslist = []
    obuselist = []
    segid = []
    segbid = []
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
                for check_data in checklist:
                    if check_data[1][0]<mindis:
                        mindis = check_data[1][0]
                        minuse = check_data[1]
                        minfs = [check_data[0], minuse[1]]
                        minsegid = check_data[1][1].getID()
                        minsegbid = check_data[1][1].getbID()

                fslist.append(minfs)
                obuselist.append(minuse)
                segid.append(minsegid)
                segbid.append(minsegbid)
                dislist.append(mindis)

            else:
                minuse = checklist[0][1]
                mindis = minuse[0]
                minfs = [checklist[0][0], minuse[1]]
                minsegid = minuse[1].getID()
                minsegbid = minuse[1].getbID()

                fslist.append(minfs)
                obuselist.append(minuse)
                segid.append(minsegid)
                segbid.append(minsegbid)
                dislist.append(mindis)

        else:
            minfs = []
            minuse = []
            minsegid = None
            minsegbid = None
            mindis = None

            fslist.append(minfs)
            obuselist.append(minuse)
            segid.append(minsegid)
            segbid.append(minsegbid)
            dislist.append(mindis)
        # print (len(segid))
    return  obuselist,segid,segbid,fslist,dislist

want = matchGPStoRoad(pf,fsegmentList,froadList,30)
print ("开始分类")
pf['SegID'] = want[1]
pf['RoadID'] = want[2]
pf['Disto_Seg'] = want[4]
pf.to_csv('street_Classified.csv')
# obuselist = want[0]
# #去有用点的匹配子路段数据结构
# fseg_uselist = []
# for ob_usedata in obuselist:
#     if ob_usedata != []:
#         fseg_data  = ob_usedata[1]
#         fseg_uselist.append(fseg_data)
# print (len(fseg_uselist),fseg_uselist)
endTime = datetime.datetime.now()
print('本次程序运行时间为：', endTime-startTime)