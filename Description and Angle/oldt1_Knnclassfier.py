import numpy as np
import pandas as pd
import getdata as gd
import time
from sklearn import tree,neighbors

jsonURL = 'street2.json'
jsondata = pd.read_json(jsonURL)
roadList = gd.GetData.getRoadlist(jsondata)
sroadList = gd.GetData.getSRoadlist(roadList)
crossList = gd.GetData.getCrosslist(roadList)
segmentList = gd.GetData.getsegmentlist(roadList,crossList)
jointList = gd.GetData.getJointlist(segmentList,crossList)

X = []
Y = []
nX = []
nY = []
for data in sroadList:
    for i in np.arange(len(data.getMoreData(5))):
        X.append(data.getMoreData(5)[i])
        Y.append(data.getID())

X = np.array(X)
Y = np.array(Y)

# mean = X.mean(axis = 0)
# std = X.std(axis = 0)
# X = (X-mean)/std

idx = np.arange(X.shape[0]) ##X.shape[0]表示矩阵X的行数，idx返回array[0,行数-1]
np.random.seed(13) ##使随机数据可预测
np.random.shuffle(idx) ##随机打乱矩阵（洗牌）无返回值
X = X[idx]
y = Y[idx]

print (len(X),len(y))
##采用切片方法，抽取75%作为训练集，25%为测试集
X_train = X[:int(X.shape[0]*0.75)]
y_train = y[:int(X.shape[0]*0.75)]
X_test = X[int(X.shape[0]*0.75):]
y_test = y[int(X.shape[0]*0.75):]

clf = neighbors.KNeighborsClassifier(n_neighbors = 5,weights = 'uniform').fit(X_train,y_train)
# clf = tree.DecisionTreeClassifier().fit(X_train,y_train)
#==============================================================================
# pre = clf.predict(X_test)
# print (metrics.classification_report(y_test,pre))
#==============================================================================

iURL2 = 'street2.csv'
csvdata = pd.read_csv(iURL2)
usefuldata = csvdata.loc[ :,["Lon","Lat"]]

# mean = usefuldata.mean(axis = 0)
# std = usefuldata.std(axis = 0)
# usefuldata = (usefuldata-mean)/std

segID_pre = clf.predict(usefuldata)
#print (roadID_pre)
##思路：在CSV文件Dataframe加入一列RoadID对应roadID_pre
csvdata["SroadID_pre"] = segID_pre
csvdata.to_csv('street_add.csv')

