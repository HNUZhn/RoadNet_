from getdata import *
from theFunctions import *
from Class import *

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
froadlist = GetData.getFRoadlist(roadList,0.0025,25)#0.0025为可容忍道路之间距离约200米，25为可容忍平行路段角度差**可增加Score其他参数
fcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[0]
notrealcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[1]
notrealdoublelist = GetData.getFCrosslist(roadList,0.0025,25)[2]
fsegmentList = GetData.getFsegmentlist(roadList,0.0025,25)

for datafs in fsegmentList:
    if datafs.getbID() is None:
        print (datafs.getCordinations())
print('路网条数有：', len(roadList))
print('道路条数有：',len(sroadList))
print('FRoad条数有：',len(froadlist))
print('交叉点个数：', len(crossList))
print('FCross个数：',len(fcrosslist))
print('NCross个数：',len(notrealcrosslist))
print('子路段个数为：', len(segmentList))
print('FSeg个数为:',len(fsegmentList))
print('Seg新增：',len(notrealdoublelist))
print('Joint点长度为：', len(jointList))
fi = 0
fz = 0
for f in froadlist:
    if len(f.getSonRoads())>2:
        print (f)
    if len(f.getSonRoads()) == 2:
        fi = fi+1
    if len(f.getSonRoads()) == 1:
        fz = fz+1
print("单行道有%s条，双行道有%s条"%(fz,fi))
def standardAnalysis(roadList,num):
    i = 0
    for data in roadList:
        # print('路段%s的均值标准差分数' % data.getID(), data.getScore())
        if data.getScore()[1] > num:
            i += 1
    rate = round(i / len(roadList), 2)
    return "标准差大于%s的比例："%num, rate

def scoreAnalysis(roadList,num):
    i = 0
    for data in roadList:
        # print('路段%s的均值标准差分数' % data.getID(), data.getScore())
        if data.getScore()[2] > num:
            i += 1
    rate = round(i / len(roadList), 2)
    return "道路长度加权后的标准差大于%s的比例："%num, rate

def filterlist(sameroadlist,l):
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
                if imd[2]<jmd[2]:
                    md_fin2.remove(jmd)
                elif imd in md_fin2:
                    md_fin2.remove(imd)
    # md_fin = md_fin2
    # for mi in md_fin:
    #     for mj in md_fin:
    #         if mi != mj :
    #             z = [k for k in mi[0:2] if k not in mj[0:2]]
    #             if len(z)>0:
    #                 if mi[2] > mj[2]:
    #                     if mi in md_fin2:
    #                         md_fin2.remove(mi)
    #                 else:
    #                     if mj in md_fin2:
    #                         md_fin2.remove(mj)
    return md_fin2


sA = standardAnalysis(roadList,10)
scA = scoreAnalysis(roadList,10)
fl = filterlist(s,0.0035)
print (sA,scA)
print(fl)
print (len(fl))

dissameroadlist = []
for i in range(len(fl)):
    list_i = fl[i][0:2]
    dissameroadlist.append(list_i)

idlist = []
for id in dissameroadlist:
    idinlist = []
    for d in id:
        idinlist.append(d.getID())
    idlist.append(idinlist)
print (idlist)


angelesameroadlist = []
for road_data in dissameroadlist:
    if (road_data[0].getScore()[0] - 25 < road_data[1].getScore()[0] < road_data[0].getScore()[0] + 25) | \
            (road_data[0].getScore()[0] - 25 < road_data[1].getScore()[0] - 180 < road_data[0].getScore()[0] + 25) | \
            (road_data[0].getScore()[0] - 25 < road_data[1].getScore()[0] + 180 < road_data[0].getScore()[0] + 25):
        angelesameroadlist.append(road_data)
print(len(angelesameroadlist))

idlist_1 = []
for id in angelesameroadlist:
    idinlist_1 = []
    for d in id:
        idinlist_1.append(d.getID())
    idlist_1.append(idinlist_1)
print (idlist_1)

finnal_list = GetData.tolist(angelesameroadlist)

idlist_2 = []
for id2 in finnal_list:
    idlist_2.append(id2.getID())
idlist_2.sort()
print (idlist_2)

for rds in finnal_list:
    i = 0
    for rds2 in finnal_list:
        if rds == rds2:
            i += 1
            if i>=2:
                print (rds.getID())

print(len(s))
print(len(finnal_list))

unusefullist = []
for sl in s:
    if sl not in finnal_list:
        unusefullist.append(sl)

