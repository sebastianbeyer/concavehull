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
from matplotlib.path import Path
import lineintersect as li

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
    plt.axis('equal')
    plt.axis([min(dataset[:,0])-0.5,max(dataset[:,0])+0.5,min(dataset[:,1])-0.5,
        max(dataset[:,1])+0.5])
    plt.show()

def plotPath(dataset, path):
    plt.plot(dataset[:,0],dataset[:,1],'o')
    path = np.asarray(path)
    plt.plot(path[:,0],path[:,1],'-')
    plt.axis('equal')
    plt.axis([min(dataset[:,0])-0.5,max(dataset[:,0])+0.5,min(dataset[:,1])-0.5,
        max(dataset[:,1])+0.5])
    plt.show()

def removePoint(dataset, point):
    delmask = [np.logical_or(dataset[:,0]!=point[0],dataset[:,1]!=point[1])]
    newdata = dataset[delmask]
    return newdata


def concaveHull(dataset, k):
    assert k >= 3, 'k has to be greater or equal to 3.'
    points = dataset
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
    # set prevPoint to a Point directly below currentpoint (angle=0)
    prevPoint = (currentPoint[0]+10, currentPoint[1])
    step = 2

    while ( (not np.array_equal(firstpoint, currentPoint) or (step==2)) and points.size > 0 ):
        if ( step == 5 ): # we're far enough to close too early
            points = np.append(points, [firstpoint], axis=0)
        kNearestPoints = GetNearestNeighbors(points, currentPoint, k)
        cPoints = SortByAngle(kNearestPoints, currentPoint, prevPoint)
        # avoid intersections: select first candidate that does not intersect any
        # polygon edge
        its = True
        i = 0
        while ( (its==True) and (i<cPoints.shape[0]) ):
                i=i+1
                if ( np.array_equal(cPoints[i-1], firstpoint) ):
                    lastPoint = 1
                else:
                    lastPoint = 0
                j = 2
                its = False
                while ( (its==False) and (j<np.shape(hull)[0]-lastPoint) ):
                    its = li.doLinesIntersect(hull[step-1-1], cPoints[i-1],
                            hull[step-1-j-1],hull[step-j-1])
                    j=j+1
        if ( its==True ):
            # todo: still intersections: recursive restart with higher k:
            print "all candidates intersect -- restart with larger k"
            #return concaveHull(points2,k+1)
        prevPoint = currentPoint
        currentPoint = cPoints[i-1]
        # add current point to hull
        hull.append(currentPoint)
        points = removePoint(points,currentPoint)
        step = step+1
    # check if all points are inside the hull
    p = Path(hull)
    pContained = p.contains_points(dataset, radius=0.0000000001)
    if (not pContained.all()):
        print "not all points of dataset contained in hull -- restart with larger k"

    print "finished with k = ",k
    return hull


############################################################
## tests
############################################################

nx = 5
ny = nx
tpoints = []
tpointsy = []
x = np.arange(nx)
for i in x:
        tpoints.append((i,0))
        tpointsy.append((0,i))
tpoints = np.asarray(tpoints)
tpointsy = np.asarray(tpointsy)

def test_GetNearestNeighbors_1d_x_00():
    neighbors = GetNearestNeighbors(tpoints, (0,0),nx)
    assert np.array_equal(neighbors,tpoints)
def test_GetNearestNeighbors_1d_x_nx():
    neighbors = GetNearestNeighbors(tpoints, (nx,nx),nx)
    assert np.array_equal(neighbors,tpoints[::-1])

def test_GetNearestNeighbors_1d_y_00():
    neighbors = GetNearestNeighbors(tpointsy, (0,0),nx)
    assert np.array_equal(neighbors,tpointsy)
def test_GetNearestNeighbors_1d_y_nx():
    neighbors = GetNearestNeighbors(tpointsy, (nx,nx),nx)
    assert np.array_equal(neighbors,tpointsy[::-1])


################################################
clock = np.array([[3,2], [4,2], [4,3], [4,4], [3,4], [2,4], [2,3], [2,2]])

def check_SortByAngle(points,currentPoint,prevPoint,i):
    sortedPoints = SortByAngle(points,currentPoint,prevPoint)
    #for j in np.arange(len(clock)):
    #    print sortedPoints[j], clock[j], np.roll(clock,-i,axis=0)[j]
    assert np.array_equal(sortedPoints, np.roll(clock,-i,axis=0))

def test_SortByAngle_clock():
    i=0
    for point in clock:
        yield check_SortByAngle, clock, (3,3), point, i
        i=i+1

################################################
# test dataset
points = np.array([[10,  9], [ 9, 18], [16, 13], [11, 15], [12, 14], [18, 12],
                   [ 2, 14], [ 6, 18], [ 9,  9], [10,  8], [ 6, 17], [ 5,  3],
                   [13, 19], [ 3, 18], [ 8, 17], [ 9,  7], [ 3,  0], [13, 18],
                   [15,  4], [13, 16]])

points_solution_k_5 = np.array([[5, 1],[6, 2],[7, 3],[6, 4],[5, 5],[4, 4],
                                [3, 3],[4, 2],[5, 1]])

def test_concaveHull_1_k_5():
    hull = concaveHull(points,5)
    assert np.array_equal(hull, points_solution_k_5)


# add some noise

noise = np.random.normal(0,0.5,points.size)
noise = noise.reshape(points.shape)
#points = points+noise


# test
points = np.array([[ 5,  1], [ 6,  2], [ 7,  3], [ 6,  4], [ 5,  5], [ 4,  4],
                   [ 3,  3], [ 4,  2]])

points2 = points
points = points[::-1]


