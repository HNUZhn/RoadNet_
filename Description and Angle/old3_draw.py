import getdata as gd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

roadname = "金田路"
jsonURL = 'street2.json'
jsondata = pd.read_json(jsonURL)
roadList = gd.GetData.getRoadlist(jsondata)
sroadList = gd.GetData.getSRoadlist(roadList)
crossList = gd.GetData.getCrosslist(roadList)
segmentList = gd.GetData.getsegmentlist(roadList,crossList)
jointList = gd.GetData.getJointlist(segmentList,crossList)
NeighborSegment = gd.GetData.getNeighborSegment(segmentList,[114.0378885, 22.5589664])
jtroad = gd.GetData.searchroad(jsondata,roadname)
print('路网条数有：',len(roadList))
print('交叉点个数：',len(crossList))
print('子路段个数为：',len(segmentList))
print('Joint点长度为：',len(jointList))
print('交叉点子路段：',NeighborSegment)
print('%s采样路段个数:'%roadname,len(jtroad))

import pandas as pd
pf = pd.read_csv('street_GPSTimeDivide.csv')
obdata = pf[pf['ObjectID']== 31334]
obdata_26 = obdata[obdata['Day']==26]
obdata_useful = obdata_26[obdata_26['Hour'] == 16]
obdata_useful = obdata_useful.sort_values(by =['Hour','Min','Sec'])

print("开始作图")
for item in segmentList:
    LonX = list(zip(*item.cordinations))[0]
    LatY = list(zip(*item.cordinations))[1]
    #print(LonX)
    plt.plot(LonX,LatY,c='k', linestyle='-', label='Road',linewidth=3, alpha=0.5)

plt.scatter(obdata_useful['Lon'],obdata_useful['Lat'],c = 'b',s = 20, alpha = 0.7)
plt.plot(obdata_useful['Lon'],obdata_useful['Lat'],c='k',linestyle='-', label='Road',linewidth=1, alpha=0.7)

for sroadID,sroadDirect in zip(obdata_useful['SroadID_pre'],obdata_useful['Direct']):
    for sdata in sroadList:
        if sroadID == sdata.getID():
            sonlist = sdata.getSonRoads()
            sonIDlist = []
            for sr in sonlist:
                sid = sr.getID()
                sonIDlist.append(sid)
            if len(sonIDlist) == 1:
                for item in roadList:
                    if item.getID() in sonIDlist:
                        LonX = list(zip(*item.cordinations))[0]
                        LatY = list(zip(*item.cordinations))[1]
                        plt.plot(LonX,LatY,c='r', linestyle='-', label='Road',linewidth=3, alpha=0.7)
            else:
                for sonid in sonIDlist:
                    for item2 in roadList:
                        if item2.getID() == sonid:
                            if item2.getScore()[0]-20 < sroadDirect < item2.getScore()[0]+20:
                                print(item2.getDescription(),item2.getScore()[0],sroadDirect,sonid)
                                LonX1 = list(zip(*item2.cordinations))[0]
                                LatY1 = list(zip(*item2.cordinations))[1]
                                plt.plot(LonX1, LatY1, c='r', linestyle='-', label='Road', linewidth=3, alpha=0.7)

plt.show()