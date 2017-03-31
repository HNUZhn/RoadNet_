import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    xlist.append(a + z / 2)
    countlist.append( pf_count)

plt.bar(xlist, countlist, align='center', yerr=0.000001)
plt.ylabel('Frequency')
plt.show()
