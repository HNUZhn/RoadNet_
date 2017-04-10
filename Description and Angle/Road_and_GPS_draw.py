# -*- coding:utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
from readdata import *
import math
import matplotlib
from getdata import *


jsonURL = 'street2.json'
# jsonURL = 'C:\\Users\\Cimucy\\Documents\\Tencent Files\\737728114\\FileRecv\\hnumap1.json'
jsondata = pd.read_json(jsonURL)
buildingList = GetData.getBuilding(jsondata)
zhfont1 = matplotlib.font_manager.FontProperties(fname=r'C:\windows\Fonts\STSong.ttf')#设置字体方法
for item in fsegmentList:
    if item.description is None:
        LonX = list(zip(*item.cordinations))[0]
        LatY = list(zip(*item.cordinations))[1]
        plt.plot(LonX, LatY, c='k', linestyle='-', label='Road', linewidth=2, alpha=0.5)
    # plt.text((item.getHead()[0] + item.getTail()[0]) / 2, (item.getHead()[1] + item.getTail()[1]) / 2, item.getID(), color='r', alpha=0.5)
    # plt.annotate(item.getID(), ((item.getHead()[0] + item.getTail()[0]) / 2, (item.getHead()[1] + item.getTail()[1]) / 2),xytext = ((item.getHead()[0] + item.getTail()[0]) / 2, (item.getHead()[1] + item.getTail()[1]) / 2))

# for item in segmentList:
#     LonX = list(zip(*item.cordinations))[0]
#     LatY = list(zip(*item.cordinations))[1]
#     plt.plot(LonX, LatY, c='k', linestyle='-', label='Road', linewidth=2, alpha=0.5)
#     plt.text((item.getHead()[0] + item.getTail()[0]) / 2, (item.getHead()[1] + item.getTail()[1]) / 2, item.getID(), color='r', alpha=0.5)
def getColorbyDirect(direct):
    if direct<30:
        color = '#E60012'
    elif direct<60:
        color = '#F39800'
    elif direct<90:
        color = '#FFF100'
    elif direct<120:
        color = '#8FC31F'
    elif direct<150:
        color = '#009944'
    elif direct<180:
        color = '#009E96'
    elif direct<210:
        color = '#00A0E9'
    elif direct<240:
        color = '#0068B7'
    elif direct<270:
        color = '#1D2088'
    elif direct<300:
        color = '#920783'
    elif direct<330:
        color = '#E4007F'
    else:
        color = '#E5004F'
    return color
for itemr in roadList:
    color = getColorbyDirect(itemr.getScore()[0])
    LonXr = list(zip(*itemr.cordinations))[0]
    LatYr = list(zip(*itemr.cordinations))[1]
    plt.plot(LonXr, LatYr, c=color, linestyle='-', label='Road', linewidth=2, alpha=0.5)
    if "name" in itemr.getDescription():
        plt.text(itemr.getMiddleCordination()[0], itemr.getMiddleCordination()[1],itemr.description["name"],
                 color=color, alpha=0.8,fontproperties=zhfont1)
        # plt.annotate(itemr.description["name"],(itemr.getMiddlePoint()),
        #              xytext=(itemr.getMiddlePoint()),fontproperties=zhfont1)

for itemb in buildingList:
    if len(itemb.cordinations)!=1:
        continue
    LonXb = list(zip(*itemb.cordinations[0]))[0]
    LatYb = list(zip(*itemb.cordinations[0]))[1]
    plt.plot(LonXb,LatYb,c='k', linestyle='-', label='Building', linewidth=2, alpha=0.5)

pf = pd.read_csv("street_Classified.csv")

pf5 = pf[pf["RoadID"] == 5]
pf5 = pf5[pf5["Speed"] !=0 ]
# pf5 = pf5[pf5["Day"] ==16 ]
meanspeed5 = pf5["Speed"].mean()
print("RoadID位5的平均速度",round(meanspeed5,2))
plt.scatter(pf5["Lon"],pf5["Lat"],c= 'r',s=5,alpha = 0.7)
pf176 = pf[pf["RoadID"] == 176]
pf176 = pf176[pf176["Speed"] !=0 ]
meanspeed176 = pf176["Speed"].mean()
print("RoadID位176的平均速度",round(meanspeed176,2))
plt.scatter(pf176["Lon"],pf176["Lat"],c= 'b',s=5,alpha = 0.7)
plt.show()

import win32com.client                           #文字转语音
speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Speak("金田路的平均速度为%s"%round(meanspeed5,2))
