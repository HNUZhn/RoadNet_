from getdata import *
from theFunctions import *
from Class import *
import operator

# roadname = '福中三路'
jsonURL = 'street2.json'
# # jsonURL = 'CS.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList, crossList)
# sroadList = GetData.getSRoadlist(segmentList)
# jointList = GetData.getJointlist(segmentList, crossList)
# jtroad = GetData.searchroad(jsondata, roadname)
# print(jtroad)
# print(len(jtroad))
#
# import re
# def searchroad2(roadList, roadname):
#     ID = []
#     for data in roadList:
#         if 'name' in data.description:
#             if re.match(roadname, data.description['name']) != None:
#                 ID.append(data.getID())
#     return ID
#
# b = searchroad2(roadList,roadname)
# print (b)
# for i in jtroad:
#     p_x = list(zip(*i))[0]
#     p_y = list(zip(*i))[1]
#     x = sum(p_x) / len(i)
#     y = sum(p_y) / len(i)
#     list_mp = [x, y]
#     print (list_mp)
# a = ((114.05139369473684-114.05097223043477)**2+(22.54544332631579-22.545298626086957)**2)**0.5
# print (a)
#
# for j in roadList:
#     if j.getID() in b:
#         print(j.getScore())
# print(278.5-(76.8+180))

# import pandas as pd
# import matplotlib.pyplot as plt
# pf = pd.read_csv('street_SZ.csv')
# obdata = pf[pf['ObjectID'] == 117750]
# obdata_26 = obdata[obdata['Day']==31]
# obdata_useful = obdata_26[obdata_26['Hour'] == 17]
# obdata_useful = obdata_useful.sort_values(by =['Hour','Min','Sec'])
# obdata_useful = obdata_useful[obdata_useful['Speed'] != 0]
# obxy = obdata_useful.loc[ :,["Lon","Lat","Direct","Speed"]]
# print(obxy)
#
# plt.scatter(obdata_useful['Lon'],obdata_useful['Lat'],s = 50,c = 'r')
# for c in segmentList:
#     LonX = list(zip(*c.cordinations))[0]
#     LatY = list(zip(*c.cordinations))[1]
#     plt.plot(LonX, LatY, 'k')
# obid = []
# for data in pf['ObjectID']:
#     if data not in obid:
#         obid.append(data)
# print (obid)
# plt.show()


a = [1,2,3]

n = len(a)
for i in range(n) :
    if a[i] ==2:
        a.insert(2,2)
        print ("插入2",len(a))
        n += 1
    if len(a) >10:
        print (len(a))
        break

print (a)

def get_min_CP(seg, P):
    minD = []
    minD_C = []
    tempHeadC = []
    temp1 = 0
    tempList1 = []
    tempList2 = []
    tempList3 = []
    for itemC in seg:
        if len(tempHeadC) != 0:
            tempList1.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[0])
            tempList2.append(get_Distance_and_Coordinate(tempHeadC, itemC, P)[1])
            tempList3.append([tempHeadC, itemC])

            # print(get_Distance_and_Coordinate(tempHeadC, itemC, P))
            # print(tempList2)
        tempHeadC = itemC
    minD = min(tempList1)
    minD_C= tempList2[tempList1.index(min(tempList1))]
    minD_app = tempList3[tempList1.index(min(tempList1))]

    return minD, minD_C, minD_app

seg = [[-1,3],[6,6],[8,8]]
P = [4,1]
cp = get_min_CP(seg,P)
print (cp)

def getFCrosslist(roadlist, dis, divang):
    froadlist = GetData.getFRoadlist(roadlist, dis, divang)
    fcList = []
    fnlist = []
    crossList = GetData.getCrosslist(roadlist)
    for data in froadlist:
        if len(data.getCordinations()) == 2:
            for cdata in crossList:
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
                    fcList.append([point, cdata])
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
                    fcList.append([point, cdata])
                else:
                    pass
                    # 交叉点会有重复的，去重。set好像不支持二维列表。
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

    return fcrosslist, notrealcrosslist, notrealdoublelist

aaa = [1,2,3,4,5]
bbb = [1,2]
ccc = [2,1]

if bbb in aaa:
    print("正的对")
if ccc in aaa:
    print("反过来对")
else:print("反过来不对")