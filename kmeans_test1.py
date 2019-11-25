# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 09:56:05 2019

@author: cwaldoch
"""

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd

df = pd.read_csv(r"C:\Users\cwaldoch\Desktop\sfhss\utility_dash-master\utility_dash-master\utility_stats.csv")
df = df[df['Total MW'] >= 100]
df2 = df[['Weighted Age', 'Utility-Em']]
#df3 = df2[df2['DDP_MW'].notnull()]
df3 = df2
#distortions = []
#
#for i in range(1,11):
#    print('kmeans iteration '+str(i))
#    km = KMeans(
#            n_clusters=i, init='random',
#            n_init=10, max_iter=300,
#            tol=1e-04, random_state=0)
#    
#    km.fit(df3)
#    distortions.append(km.inertia_)
#    
#    
#plt.plot(range(1,11), distortions, marker='o')
#plt.xlabel('Number of clusters')
#plt.ylabel('Distortion')
#plt.show()

km = KMeans(
        n_clusters=6, init='random',
        n_init=10, max_iter=1000,
        tol=1e-04, random_state=0)

y_km = km.fit_predict(df3)

plt.scatter(df3['Weighted Age'], df3['Utility-Em'], c=km.labels_.astype(float), s=50, alpha=0.5)

centroids = km.cluster_centers_
plt.scatter(centroids[:,0], centroids[:,1], label='centroids',c='red', s=50)
plt.xlabel('Capacity-weighted Portfolio Age')
plt.ylabel('Capacity-Weighted CO2 Rate per MMBTU')
plt.legend()
plt.savefig('kmeans_utilities_6_filtered.png', dpi=300)