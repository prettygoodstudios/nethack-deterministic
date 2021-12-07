
import math


def furthestDistanceFromMean(a, n):
    sum = a.findMeanVisitedPosition()
    pNode = [n.x, n.y]
    pAgent = [sum[0], sum[1]]
    distance = math.sqrt( ((pNode[0]-pAgent[0])**2)+((pNode[1]-pAgent[1])**2) )
    return -distance
