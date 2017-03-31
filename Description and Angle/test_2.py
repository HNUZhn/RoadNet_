from getdata import *
import pickle
import pandas as pd

jsonURL = 'street2.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList, crossList)
froadList = GetData.getFRoadlist(roadList,0.0025,25)
fcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[0]
notrealcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[1]
fsegmentList = GetData.getFsegmentlist(roadList,0.0025,25)
fjointList = GetData.getJointlist(fsegmentList, fcrosslist)
notrealdoublelist = GetData.getFCrosslist(roadList,0.0025,25)[2]

print('路网条数有：', len(roadList))
print('FRoad条数有：',len(froadList))
print('交叉点个数：', len(crossList))
print('FCross个数：',len(fcrosslist))
print('NCross个数：',len(notrealcrosslist))
print('子路段个数为：', len(segmentList))
print('FSeg个数为:',len(fsegmentList))
print("FJoint个数为：",len(fjointList))
print('Seg新增：',len(notrealdoublelist))

for data in fjointList:
    if data is None:
        print ("chucuo")
i = 0
for data in fsegmentList:
    if data.getbID() is None:
        i+=1
print (i)