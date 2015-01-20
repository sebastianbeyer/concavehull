#!/bin/env python

##
## determine if two line segments intersect
## see: martin-thoma.com/how-to-check-if-two-line-segments-intersect/
##

import numpy as np

def doBoundingBoxesIntersect(a, b, c, d):
    '''
    Check if bounding boxes do intersect. If one bounding box touches
    the other, they do intersect.
    First segment is of points a and b, second of c and d.
    '''
    return a[0] <= d[0] and \
           b[0] >= c[0] and \
           a[1] <= d[1] and \
           b[1] >= c[1]

def isPointOnLine(a,b,c):
    '''
    Check if a point is on a line.
    '''
    # move to origin
    aTmp = (0,0)
    bTmp = (b[0] - a[0], b[1] - a[1])
    cTmp = (c[0] - a[0], c[1] - a[1])
    r = np.cross(bTmp, cTmp)
    return np.abs(r) < 0.000001

def isPointRightOfLine(a,b,c):
    '''
    Check if a point (c) is right of a line (a-b).
    If (c) is on the line, it is not right it.
    '''
    # move to origin
    aTmp = (0,0)
    bTmp = (b[0] - a[0], b[1] - a[1])
    cTmp = (c[0] - a[0], c[1] - a[1])
    return np.cross(bTmp, cTmp) < 0

def lineSegmentTouchesOrCrossesLine(a,b,c,d):
    '''
    Check if line segment (a-b) touches or crosses
    line segment (c-d).
    '''
    return isPointOnLine(a,b,c) or \
           isPointOnLine(a,b,d) or \
          (isPointRightOfLine(a,b,c) and
           isPointRightOfLine(a,b,d))

def doLinesIntersect(a,b,c,d):
    '''
    Check if line segments (a-b) and (c-d) intersect.
    '''
    return doBoundingBoxesIntersect(a,b,c,d) and \
           lineSegmentTouchesOrCrossesLine(a,b,c,d) and \
           lineSegmentTouchesOrCrossesLine(c,d,a,b)





##############################
## Tests
##############################

def test_doBoundingBoxesIntersect():
    A=(1,1); B=(2,2); C=(3,1); D=(4,2)
    assert doBoundingBoxesIntersect(A,B,C,D) == False
    A=(1,2); B=(3,4); C=(2,1); D=(4,3)
    assert doBoundingBoxesIntersect(A,B,C,D) == True

def test_isPointOnLine():
    A=(1,1); B=(3,3); C=(2,2)
    assert isPointOnLine(A,B,C) == True
    A=(1,1); B=(3,3); C=(3,2)
    assert isPointOnLine(A,B,C) == False


def test_isPointRightOfLine():
    A=(1,1); B=(3,3); C=(2,2)
    assert isPointRightOfLine(A,B,C) == False
    A=(1,1); B=(3,3); C=(3,2)
    assert isPointRightOfLine(A,B,C) == True
    A=(1,1); B=(3,3); C=(1,2)
    assert isPointRightOfLine(A,B,C) == False




