#!/bin/env python

##
## check performance of concavehull
##

import numpy as np
import matplotlib.pyplot as plt
import ConcaveHull as CH
import timeit


nmax = 10000

alldata = np.random.randint(0,5*nmax,size=2*nmax)
alldata = alldata.reshape(nmax,2)


times = []
nrange = np.arange(1000,nmax+1000,1000)

for n in nrange:
    print "--- n = ",n," ---"
    data = alldata[:n]
    time = timeit.timeit("CH.concaveHull(data,20)",setup="import ConcaveHull as CH; \
                         from __main__ import data",number=1)
    times.append(time)

plt.plot(nrange,times)
plt.show()
