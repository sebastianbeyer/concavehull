#!/bin/env python

##
## calculate the concave hull of a set of points
## see: CONCAVE HULL: A K-NEAREST NEIGHBOURS APPROACH
##      FOR THE COMPUTATION OF THE REGION OCCUPIED BY A
##      SET OF POINTS
##      Adriano Moreira and Maribel Yasmina Santos 2007
##

import numpy as np
import scipy.spatial as spt
import matplotlib.pyplot as plt

def GetFirstPoint(dataset):
    ''' Returns index of first point, which has the lowest y value '''
    # todo: what if there is more than one point with lowest y?
    imin = np.argmin(dataset[:,1])
    return dataset[imin]

def GetNearestNeighbors(dataset, point, k):
    ''' Returns indices of k nearest neighbors of point in dataset'''
    # todo: experiment with leafsize for performance
    mytree = spt.cKDTree(dataset,leafsize=10)
    distances, indices = mytree.query(point,k)
    # todo: something strange here, we get more indices than points in dataset
    #       so have to do this
    return dataset[indices[:dataset.shape[0]]]

def SortByAngle(kNearestPoints, currentPoint, prevPoint):
    ''' Sorts the k nearest points given by angle '''
    angles = np.zeros(kNearestPoints.shape[0])
    i = 0
    for NearestPoint in kNearestPoints:
        # calculate the angle
        angle = np.arctan2(NearestPoint[1]-currentPoint[1],
                NearestPoint[0]-currentPoint[0]) - \
                np.arctan2(prevPoint[1]-currentPoint[1],
                prevPoint[0]-currentPoint[0])

        angle = np.rad2deg(angle)
        # only positive angles
        angle = np.mod(angle+360,360)
        #print NearestPoint[0], NearestPoint[1], angle
        angles[i] = angle
        i=i+1
    return kNearestPoints[np.argsort(angles)]

def plotPoints(dataset):
    plt.plot(dataset[:,0],dataset[:,1],'o')
    plt.show()

def plotPath(dataset, path):
    plt.plot(dataset[:,0],dataset[:,1],'o')
    plt.plot(path[:,0],path[:,1],'-')
    plt.show()

def removePoint(dataset, point):
    delmask = [np.logical_or(dataset[:,0]!=point[0],dataset[:,1]!=point[1])]
    newdata = dataset[delmask]
    return newdata



k = 3
assert k >= 3, 'k has to be greater or equal to 3.'


# test dataset
points = np.array([[10,  9],
                   [ 9, 18],
                   [16, 13],
                   [11, 15],
                   [12, 14],
                   [18, 12],
                   [ 2, 14],
                   [ 6, 18],
                   [ 9,  9],
                   [10,  8],
                   [ 6, 17],
                   [ 5,  3],
                   [13, 19],
                   [ 3, 18],
                   [ 8, 17],
                   [ 9,  7],
                   [ 3,  0],
                   [13, 18],
                   [15,  4],
                   [13, 16]])

# test
#points = np.array([[ 5,  1],
#                   [ 6,  2],
#                   [ 7,  3],
#                   [ 6,  4],
#                   [ 5,  5],
#                   [ 4,  4],
#                   [ 3,  3],
#                   [ 4,  2]])
points2 = points

points = points[::-1]

# todo: remove duplicate points from dataset
# todo: check if dataset consists of only 3 or less points
# todo: make sure that enough points for a given k can be found

firstpoint = GetFirstPoint(points)

# init hull as list to easily append stuff
hull = []

# add first point to hull
hull.append(firstpoint)
# and remove it from dataset
points = removePoint(points,firstpoint)

currentPoint = firstpoint
# set prevPoint to a Point directly right of currentpoint (angle=0)
prevPoint = (currentPoint[0]+1, currentPoint[1])
step = 2

while ( (not np.array_equal(firstpoint, currentPoint) or (step==2)) and points.size > 0 ):
    print currentPoint
    print points
    print "---"
    if ( step == 5 ): # we're far enough to close too early
        points = np.append(points, [firstpoint], axis=0)
    kNearestPoints = GetNearestNeighbors(points, currentPoint, k)
    cPoints = SortByAngle(kNearestPoints, currentPoint, prevPoint)
    currentPoint = cPoints[0]
    # add current point to hull
    hull.append(currentPoint)
    prevPoint = currentPoint
    points = removePoint(points,currentPoint)
    step = step+1










