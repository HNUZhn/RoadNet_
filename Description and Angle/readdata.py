import pickle
import sys
# # 使用pickle模块将数据对象保存到文件
# sys.setrecursionlimit(1000000)
# class数据 读取部分
pkl_file = open('roadList.pkl', 'rb')
roadList = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('fjointList.pkl', 'rb')
fjointList = pickle.load(pkl_file)
pkl_file.close()


pkl_file = open('fsegmentList.pkl', 'rb')
fsegmentList = pickle.load(pkl_file)
pkl_file.close()

pkl_file = open('froadList.pkl', 'rb')
froadList = pickle.load(pkl_file)
pkl_file.close()

print('roadList  路网条数有：', len(roadList))
print('jointList  Joint点长度为：', len(fjointList))
print('fsegmentList  子路段个数为：', len(fsegmentList))
print('froadList 条数有：', len(froadList))
