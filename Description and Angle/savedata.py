from getdata import *
import pickle
import pandas as pd

jsonURL = 'street2.json'
jsondata = pd.read_json(jsonURL)
roadList = GetData.getRoadlist(jsondata)
crossList = GetData.getCrosslist(roadList)
segmentList = GetData.getsegmentlist(roadList,crossList)
froadList = GetData.getFRoadlist(roadList,0.0025,25)
fcrosslist = GetData.getFCrosslist(roadList,0.0025,25)[0]
fsegmentList = GetData.getFsegmentlist(roadList,0.0025,25)
fjointList = GetData.getJointlist(fsegmentList, fcrosslist)

print('开始保存！roadList')
output1 = open('roadList.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(roadList, output1,2)
output1.close()


print('开始保存！fsegmentList')
output2 = open('fsegmentList.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(fsegmentList, output2,2)
output2.close()


print('开始保存！fjointList')
output3 = open('fjointList.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(fjointList, output3,2)
output3.close()

print('开始保存！froadList')
output4 = open('froadList.pkl', 'wb')
# Pickle dictionary using protocol 0.
pickle.dump(froadList, output4,2)
output4.close()

print('结束保存！')