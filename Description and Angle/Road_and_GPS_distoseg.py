import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

zhfont1 = matplotlib.font_manager.FontProperties(fname=r'C:\windows\Fonts\STSong.ttf')#设置字体方法

pf = pd.read_csv("street_Classified.csv")
pf_dis = pf['Disto_Seg']
pf_dna = pf_dis.dropna(axis=0,how='any')
print (pf_dna.max(),pf_dna.min())

z = 0.00001
xlist = []
countlist = []
for a in np.arange(0,0.0005,z):
    pf_filter = pf_dna[(pf_dna>a) & (pf_dna<a+z)]
    pf_count = pf_filter.count()
    xlist.append(a+z)
    countlist.append( pf_count)
plt.hist(pf_dna,np.arange(0,0.0005,z), color = 'g', histtype='bar', rwidth=1)
plt.hist(-1*pf_dna,np.arange(-0.0005,0+z,z), color = 'g', histtype='bar', rwidth=1)
plt.plot(xlist, countlist,c = 'k',lw = 3)
plt.plot(np.arange(-0.0005,0,z),list(reversed(countlist)),c = 'k',lw = 3)
plt.plot((-z,z),(countlist[0],countlist[0]),c = 'k',lw = 3)
plt.title( r'分类后各GPS点距离对应子路段距离分布',fontsize = 18 ,fontproperties=zhfont1)
plt.ylabel('Count')
plt.xlabel('Distance')
plt.grid(True)
plt.show()
