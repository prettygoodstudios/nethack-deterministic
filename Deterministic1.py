import gym
from gym.spaces.box import Box
import nle
from nle import nethack as nh
import time
import numpy as np
from heapq import heapify, heappush, heappop
from dataclasses import dataclass, field
from typing import Any

env = gym.make("NetHackScore-v0")
obs = env.reset()
env.render()
map_objects = {}
colors = obs['colors']
map = obs['chars']
for i in range(len(map)):
    for j in range(len(map[i])):
        map_objects[map[i][j]] = colors[i][j]
blstats = [_ for _ in obs["blstats"]]
score = blstats[9]
x_pos, y_pos = blstats[0], blstats[1]
print(score)
mapAdditional = np.full((21, 79), True)

def isDoor(y, x):
    if(map[y][x] == 124 or map[y][x] == 45):
        if(colors[y][x] != 7): #Checks if not a door
            return True
    if(map[y][x] == 43):
        return True
    return False

def possibleNewRouteExists(y, x):
    if(y == 0 and x == 0):
        return mapAdditional[y+1][x] or mapAdditional[y][x+1] or mapAdditional[y+1][x+1]
    elif(y == 0):
        return mapAdditional[y][x-1] or mapAdditional[y+1][x-1] or mapAdditional[y+1][x] or mapAdditional[y][x+1] or mapAdditional[y+1][x+1]
    elif(x == 0):
        return mapAdditional[y-1][x] or mapAdditional[y-1][x+1] or mapAdditional[y+1][x] or mapAdditional[y][x+1] or mapAdditional[y+1][x+1]
    elif(y == 20 and x == 78):
        return mapAdditional[y-1][x] or mapAdditional[y][x-1] or mapAdditional[y-1][x-1]
    elif(y == 20):
        return mapAdditional[y-1][x] or mapAdditional[y][x-1] or mapAdditional[y-1][x-1] or mapAdditional[y-1][x+1] or mapAdditional[y][x+1]
    elif(x == 78):
        return mapAdditional[y-1][x] or mapAdditional[y][x-1] or mapAdditional[y-1][x-1] or mapAdditional[y+1][x-1] or mapAdditional[y+1][x]
    else:
        return mapAdditional[y-1][x-1] or mapAdditional[y-1][x] or mapAdditional[y-1][x+1] or mapAdditional[y][x-1] or mapAdditional[y][x+1] or mapAdditional[y+1][x-1] or mapAdditional[y+1][x] or mapAdditional[y+1][x+1]

def identifyPossibleNewRoutes():
    #Scan over map, check map additional
    locations = []
    for y in range(21):
        for x in range(79):
            if(possibleNewRouteExists(y, x) and isNotWall(y, x) and not map[y][x] == 32):
                locations.append((y, x))
    return locations

def isNotWall(y, x, diagonal=True): #Treats boulders as walls
    if(map[y][x] == 96):
        return False
    if(map[y][x] == 124 or map[y][x] == 45):
        if(colors[y][x] == 7): #Checks if not a door
            return False
        elif(diagonal): #Cannot move diagonally into doorways
            return False
    return True

def getPossibleMoves(y, x):
    possibleSteps = []
    coords = []
    #check up (N)
    if(y > 0):
        if(isNotWall(y-1, x)): #Wall isn't in the way
            if(map[y-1][x] == 43): #Locked door, need to kick
                possibleSteps.append([20, 1, 1])
            possibleSteps.append([1])
            coords.append((y-1, x))
    #check right (E)
    if(x < len(map[0])-1):
        if(isNotWall(y, x+1)): #Wall isn't in the way
            if(map[y][x+1] == 43): #Locked door, need to kick
                possibleSteps.append([20, 2, 2])
            possibleSteps.append([2])
            coords.append((y, x+1))
    #check down (S)
    if(y < len(map)-1):
        if(isNotWall(y+1, x)): #Wall isn't in the way
            if(map[y+1][x] == 43): #Locked door, need to kick
                possibleSteps.append([20, 3, 3])
            possibleSteps.append([3])
            coords.append((y+1, x))
    #check left (W)
    if(x > 0):
        if(isNotWall(y, x-1)): #Wall isn't in the way
            if(map[y][x-1] == 43): #Locked door, need to kick
                possibleSteps.append([20, 4, 4])
            possibleSteps.append([4])
            coords.append((y, x-1))
    
    #check up right (NE)
    if(y > 0 and x < len(map[0])-1):
        if(isNotWall(y-1, x+1, diagonal=True)):
            possibleSteps.append([5])
            coords.append((y-1, x+1))
    #check down right (SE)
    if(y < len(map)-1 and x < len(map[0])-1):
        if(isNotWall(y+1, x+1, True)):
            possibleSteps.append([6])
            coords.append((y+1, x+1))
    #check down left (SW)
    if(y < len(map)-1 and x > 0):
        if(isNotWall(y+1, x-1, True)):
            possibleSteps.append([7])
            coords.append((y+1, x-1))
    #check up left (NW)
    if(y > 0 and x > 0):
        if(isNotWall(y-1, x-1, True)):
            possibleSteps.append([8])
            coords.append((y-1, x-1))
    return possibleSteps, coords

for y in range(21):
    for x in range(79):
        mapAdditional[y][x] = (map[y][x] == 32 or isDoor(y, x))

# for i in range(21):
#     for j in range(79):
#         print(int(mapAdditional[i][j]), end=" ")
#     print()

# temp = itentifyPossibleNewRoutes()

# for item in temp:
#     print(item)
#     print(map[item[0]][item[1]])


def search(pos, goal):
    distance = {str(pos): 0}
    searchSet = []
    heapify(searchSet)
    cameFrom = {pos: None}
    for i in range(21):
        for j in range(79):
            if((i,j) != pos):
                distance[str((i,j))] = float('inf')
                cameFrom[str((i,j))] = None
            heappush(searchSet, (distance[str((i,j))], (i,j)))
    while(len(searchSet) != 0):
        next = heappop(searchSet)
        #DONE
        # print(next[1][0], next[1][1])
        _, coords = getPossibleMoves(next[1][0], next[1][1])
        for coord in coords:
            possible = 1 + distance[str(next[1])]
            if(possible < distance[str(coord)]):
                distance[str(coord)] = possible
                cameFrom[str(coord)] = str(next[1])
        return distance, cameFrom
                
# dist, frm = search((y_pos,x_pos), (y_pos+2,x_pos+2))

# print(y_pos, x_pos)

# print(dist[str((y_pos-1, x_pos-1))])

def path(map, target):
    # if(map[str(target)] == None):
    #     return []
    path = []
    pathNotDone = True
    current = target
    while(pathNotDone):
        path.append(current)
        current = map[str(current)]
        if(current == None):
            pathNotDone = False
    print(path)


notDone = True
while(notDone):
    newRoutes = identifyPossibleNewRoutes()
    closest = float('inf')
    fromMap = None
    t = None
    for target in newRoutes:
        dist, frm = search((y_pos, x_pos), target)
        print("test", target, dist[str(target)])
        if(dist[str(target)] < closest):
            closest = dist[str(target)]
            fromMap = frm
            t = target
    print(closest)
    path(fromMap, t)
    print(t, y_pos, x_pos)
    if(fromMap == None):
        print("error")
