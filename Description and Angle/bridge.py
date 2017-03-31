from getdata import *
from theFunctions import *
from Class import *
import matplotlib.pyplot as plt

roadname = '金田路'
jsonURL = 'C:\\Users\\Cimucy\\Documents\\Python Scripts\\毕业设计\\street2.json'
# jsonURL = 'CS.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
sroadList = GetData.getSRoadlist(roadList)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList, crossList)
jointList = GetData.getJointlist(segmentList, crossList)
jtroad = GetData.searchroad(jsondata, roadname)
s = GetData.getParallelroadIDList(roadList)

bridgeList = []
for data in roadList:
    if 'bridge' in data.getDescription():
        if data.getDescription()['bridge'] == 'yes':
            print (data.getID(),data.getDescription())
            bridgeList.append(data)

for c in roadList:
    LonX = list(zip(*c.cordinations))[0]
    LatY = list(zip(*c.cordinations))[1]
    plt.plot(LonX, LatY, 'k')

for c in bridgeList:
    print(c.getAnglelist())
    print(c.getDistanceRate()[1])
    print(c.getScore())
    print(c.getDescription())
    LonX = list(zip(*c.cordinations))[0]
    LatY = list(zip(*c.cordinations))[1]
    p1, = plt.plot(LonX, LatY, 'r', lw=3)

global Intersection_Dict
global IntersectionID
Intersection_Dict = {}
IntersectionID = 0
dict1 = {'d':[], 'point_dict': {}, 'C':[], 'R':[]}
def init_Intersection_Dict(d, joint, R):  # 初始化，需要给予描述。坐标另行设置。
    global Intersection_Dict
    global IntersectionID
    IntersectionID += 1
    Intersection_Dict[IntersectionID] ={'d':[], 'point_dict': {}, 'C':[], 'R':[]}
    Intersection_Dict[IntersectionID]['d'] = d
    Intersection_Dict[IntersectionID]['point_dict'][joint.id] = joint.coordinate
    # 目前求在区域内的中心点坐标，采用的平均值
    a = list(zip(*Intersection_Dict[IntersectionID]['point_dict'].values()))
    Intersection_Dict[IntersectionID]['C'] = [sum(a[0]) / len(a[0]), sum(a[1]) / len(a[1])]
    Intersection_Dict[IntersectionID]['R'] = 0.0002


def add_Point_into_Intersection_Dict(ID, joint):  # 添加点，设置。
    global Intersection_Dict
    # Intersection_Dict[ID] = {'d': [], 'point_dict': {}, 'C': [], 'R': []}
    # Intersection_Dict[ID]['d'] = d
    Intersection_Dict[ID]['point_dict'][joint.id] = joint.coordinate
    # 目前求在区域内的中心点坐标，采用的平均值
    a = list(zip(*Intersection_Dict[ID]['point_dict'].values()))
    Intersection_Dict[ID]['C'] = [sum(a[0]) / len(a[0]), sum(a[1]) / len(a[1])]


def isin_ID(ID, jID):
    return jID in list(Intersection_Dict[ID]['point_dict'].keys())

#     return JointID in list(self.JointID_Dict.keys())
def isin_IntersactionDict(joint):
    for i in Intersection_Dict.keys():
        if isin_ID(i, joint.id):
            return True
        elif isin_C(i, joint.coordinate):
            add_Point_into_Intersection_Dict(i, joint)
            return True
    return False  # 遍历全部的Intersection，不在。或者

def isin_C(ID, jC):
    CC = Intersection_Dict[ID]['C']
    # print(type((((CC[0] - jC[0]) ** 2 + (CC[1] - jC[1]) ** 2) ** 0.5)))
    # print(type(Intersection_Dict[ID]['R'][0]))
    return (((CC[0] - jC[0]) ** 2 + (CC[1] - jC[1]) ** 2) ** 0.5) < 0.0002


for itemJ in jointList:
    if not isin_IntersactionDict(itemJ):
        init_Intersection_Dict([], itemJ, 0.0002)
print('init_Intersection_Dict 的长度为：',len(Intersection_Dict))

# for item_j in jointList:
#     c = item_j.coordinate
#     plt.scatter(c[0], c[1], c='g', s=20, alpha=1)

# for data in Intersection_Dict.values():
#     a = data['point_dict'].values()
#     a = list(a)
#     if len(a) >= 4:
#         for item in a :
#             plt.scatter(item[0],item[1],c = 'r',s = 20 ,alpha = 0.4)
#         b = data['C']
#         for itemb in b:
#             plt.scatter(b[0],b[1],c =  'b', s=50, alpha=0.6)
for data in Intersection_Dict.values():
    a = data['point_dict'].values()
    a = list(a)

    for item in a :
        plt.scatter(item[0],item[1],c = 'r',s = 20 ,alpha = 0.4)
    b = data['C']
    if len(a) >= 3:
        for itemb in b:
            p2 = plt.scatter(b[0],b[1],c =  'b', s=80, alpha=0.9)

plt.legend([p1,p2],['Bridge','Cross'],loc='upper right',scatterpoints=1)
plt.title(r'Bridge and Cross',fontsize=20)
plt.xlabel(r'${Lon} $', fontsize=16)
plt.ylabel(r'${Lat} $', fontsize=16)
plt.show()