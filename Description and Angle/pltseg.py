from getdata import *
from theFunctions import *
from Class import *
import matplotlib.pyplot as plt
import datetime
import analysisseg
# startTime = datetime.datetime.now()
roadname = "韶山路"
jsonURL = 'C:\\Users\\Cimucy\\Documents\\Python Scripts\\毕业设计\\street2.json'
# jsonURL = 'CS.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList, crossList)
sroadList = GetData.getSRoadlist(segmentList)
jointList = GetData.getJointlist(segmentList, crossList)
jtroad = GetData.searchroad(jsondata, roadname)


##根据路名获取ID相关列表
test_l = []
for jt in jtroad:
    for rd in roadList:
        if jt == rd.cordinations:
            print (rd)
            test_l.append(rd)


##根据Sroadlist获取相关ID列表
s = GetData.getParallelroadIDList(segmentList)
print (s)
for c in roadList:
    LonX = list(zip(*c.cordinations))[0]
    LatY = list(zip(*c.cordinations))[1]
    plt.plot(LonX, LatY, 'k')

for c in analysisseg.finnal_list:
    print(c.getAnglelist())
    print(c.getDistanceRate()[1])
    print(c.getScore())
    print(c.getDescription())
    LonX = list(zip(*c.cordinations))[0]
    LatY = list(zip(*c.cordinations))[1]
    plt.plot(LonX, LatY, 'r', lw=3)
print (len(s))
plt.show()

