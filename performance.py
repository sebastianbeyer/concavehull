#!/bin/env python

##
## check performance of concavehull
##

import numpy as np
import matplotlib.pyplot as plt
import ConcaveHull as CH
import timeit


n = 1000

data = np.random.randint(0,5*n,size=2*n)
data = data.reshape(n,2)


