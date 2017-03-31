from getdata import *
from theFunctions import *
from Class import *
import matplotlib.pyplot as plt
import datetime
import analysis
# startTime = datetime.datetime.now()
roadname = "韶山路"
jsonURL = 'C:\\Users\\Cimucy\\Documents\\Python Scripts\\毕业设计\\street2.json'
# jsonURL = 'CS.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
sroadList = GetData.getSRoadlist(roadList)
crossList = GetData.getCrosslist(sroadList)
segmentList = GetData.getsegmentlist(roadList, crossList)
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
s = GetData.getParallelroadIDList(roadList)
print (s)

bridgeList = []
for data_b in roadList:
    if 'bridge' in data_b.getDescription():
        if data_b.getDescription()['bridge'] == 'yes':
            print (data_b.getID(),data_b.getDescription())
            bridgeList.append(data_b)

for c in bridgeList:
    print(c.getAnglelist())
    print(c.getDistanceRate()[1])
    print(c.getScore())
    print(c.getDescription())
    LonX = list(zip(*c.cordinations))[0]
    LatY = list(zip(*c.cordinations))[1]
    p1, = plt.plot(LonX, LatY, 'b', lw=3)

for c in analysis.fsegmentList:
    if c.getDescription() is None:
        LonX = list(zip(*c.cordinations))[0]
        LatY = list(zip(*c.cordinations))[1]
        plt.plot(LonX, LatY, 'g',lw = 5)
    else:
        LonX = list(zip(*c.cordinations))[0]
        LatY = list(zip(*c.cordinations))[1]
        plt.plot(LonX, LatY, 'k')

for c in analysis.finnal_list:
    print(c.getAnglelist())
    print(c.getDistanceRate()[1])
    print(c.getScore())
    print(c.getDescription())
    LonX = list(zip(*c.cordinations))[0]
    LatY = list(zip(*c.cordinations))[1]
    p2, = plt.plot(LonX, LatY, 'r', lw=3,alpha = 0.7)
for nf in analysis.notrealcrosslist:
    plt.scatter(nf[0],nf[1],c = 'Y',s = 50,alpha =1)

print (len(s))
plt.legend([p1,p2],['Bridge','Parallel'],loc='upper right',scatterpoints=1)
plt.title(r'Bridge and Parallel',fontsize=20)
plt.xlabel(r'${Lon} $', fontsize=16)
plt.ylabel(r'${Lat} $', fontsize=16)
plt.show()

