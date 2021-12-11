# from _typeshed import _T_co
import gym
from gym.spaces.box import Box
import nle
from nle import nethack as nh
import time
import numpy as np
from heapq import heapify, heappush, heappop
from dataclasses import dataclass, field
from typing import Any
from Map import Map
from astar import findPathInGridWorld
from node import GraphEdge, GraphNode
from utils.graphs import GraphBuilder
from heuristics import closestToStairCase, furthestDistanceFromMean, furthestDistanceFromMeanAndClosestToUs
from main import MoveActions
from time import time
from sys import exit
from matplotlib import pyplot as plt
from matplotlib import patches
import traceback

from astar import Node

class Agent:
    score = 0
    x_pos = None
    y_pos = None
    env = None
    map = None
    heatmap_graph = None
    pQueue = None

    def __init__(self, type, heuristic):
        self.env = gym.make(type)
        obs = self.env.reset()
        self.map = Map(self.env, obs)
        blstats = [_ for _ in obs["blstats"]]
        self.score = blstats[9]
        self.x_pos, self.y_pos = blstats[0], blstats[1]
        self.start = (self.x_pos, self.y_pos)
        self.heatmap_graph = GraphBuilder(["heat_pos"])
        self.visited = set()
        self.locationStack = []
        self.graphNodes = {}
        self.moves = 0
        self.heuristic = heuristic
        self.done = False

    def play(self) -> bool:
        """Plays game returns true if found staircase otherwise false"""
        while True:
            if self.map.isDead():
                return "Dead", 0, self.moves
            self.buildGraph()
            path = None
            while path is None:
                if len(self.pQueue) == 0:
                    if not self.__breakGlass():
                        return False, 0, self.moves
                _, destination = heappop(self.pQueue)
                print(f"{self.graph.x},{self.graph.y} -> {destination.x},{destination.y}")
                path = self.generalGraphAStar(self.graph, destination, None)
                print(f"General Path {path}")
            moves = self.getMoves(path)
            print(moves)
            self.visited.add(path[-1])
            self.__executeMoves(moves)
            if self.done:
                return False, 0, self.moves
            self.render()
            #self.graph.plot(self.map, self, searchPoints=True)
            stairLocation = self.map.findStairs()
            if stairLocation is not None:
                print("Found Staircase")
                path = findPathInGridWorld(self.map, (self.x_pos, self.y_pos), (stairLocation[1], stairLocation[0]))
                if not path is None:
                    #self.heatmap_graph.save_graphs()
                    self.heuristic = closestToStairCase
                    stairMoves = self.getMoves(path)
                    self.__executeMoves(stairMoves)
                    self.render()
                    return True, len(findPathInGridWorld(self.map, self.start, (stairLocation[1], stairLocation[0]))), self.moves

    def __breakGlass(self):
        """Emergency algo"""
        queue = list(map(lambda x: (0, x), self.map.identifySearchPoints()))
        heapify(queue)
 
        while len(queue) > 0:
            path = None
            while path is None:
                if len(queue) == 0:
                    self.__breakGlass()
                    return True
                _, destination = heappop(queue)
                path = findPathInGridWorld(self.map, (self.x_pos, self.y_pos), tuple(reversed(destination)))
                print(f"Break path{path}")
            moves = self.getMoves(path)
            self.__executeMoves(moves)
            for _ in range(3):
                self.step(22)
            if self.done:
                return False
            self.render()
            height, width = self.map.getEnviromentDimensions()
            for x in range(max(0, self.x_pos-1), min(width, self.x_pos+1)):
                for y in range(max(0, self.y_pos-1), min(height, self.y_pos+1)):
                    if self.map.isNewRoute(self, y, x):
                        self.buildGraph()
                        return True


    def __executeMoves(self, moves: list):
        start = time()
        actionDirection = {
            MoveActions.UP.value: (0, -1),
            MoveActions.DOWN.value: (0, 1),
            MoveActions.LEFT.value: (-1, 0),
            MoveActions.RIGHT.value: (1, 0),
            MoveActions.UP_RIGHT.value: (1, -1),
            MoveActions.DOWN_LEFT.value: (-1, 1),
            MoveActions.DOWN_RIGHT.value: (1, 1),
            MoveActions.UP_LEFT.value: (-1, -1)
        }
        for move in moves:
            startX, startY = self.getX(), self.getY()
            count = 0
            while True:
                for i, m in enumerate(move):
                    if m == 20:
                        dx, dy = actionDirection[move[i+1]]
                        if not self.map.isPet(self.getY()+dy, self.getX()+dx):
                            self.step(m)
                    else:
                        self.step(m)

                count += 1
                if (startX, startY) != (self.getX(), self.getY()):
                    self.heatmap_graph.append_point("heat_pos", (self.getX(), self.getY()))
                    break
                if count > 20:
                    print(f"Move not working: {m}")
                    self.render()
                    break
        print(f"Execute Move Time: {time() - start}")

    def getX(self):
        return self.x_pos 
    
    def getY(self):
        return self.y_pos

    def getMoves(self, coords):
        steps = []
        y = 0
        x = 1
        current = coords[0]
        for i in range(1, len(coords)):
            if(coords[i][y] == current[y]-1 and coords[i][x] == current[x]+1 and current[x] < 78 and current[y] > 0):
                steps.append([5])
            elif(coords[i][y] == current[y]+1 and coords[i][x] == current[x]+1 and current[x] < 78 and current[y] < 20):
                steps.append([6])
            elif(coords[i][y] == current[y]+1 and coords[i][x] == current[x]-1 and current[x] > 0 and current[y] < 20):
                steps.append([7])
            elif(coords[i][y] == current[y]-1 and coords[i][x] == current[x]-1 and current[x] > 0 and current[y] > 0):
                steps.append([8])
            elif(coords[i][y] == current[y]-1 and current[y] > 0):
                if(self.map.isDoor(current[y]-1, current[x])): #Locked door, need to kick
                    steps.append([20, 1, 1])
                else:
                    steps.append([1])
            elif(coords[i][x] == current[x]+1 and current[x] < 78):
                if(self.map.isDoor(current[y], current[x]+1)): #Locked door, need to kick
                    steps.append([20, 2, 2])
                else:
                    steps.append([2])
            elif(coords[i][y] == current[y]+1) and current[y] < 20:
                if(self.map.isDoor(current[y]+1, current[x])): #Locked door, need to kick
                    steps.append([20, 3, 3])
                else:
                    steps.append([3])
            elif(coords[i][x] == current[x]-1) and current[x] > 0:
                if(self.map.isDoor(current[y], current[x]-1)): #Locked door, need to kick
                    steps.append([20, 4, 4])
                else:
                    steps.append([4])
            else:
                return None
            current = coords[i]
        return steps

    def getPossibleMoves(self, y, x):
        possibleSteps = []
        coords = []
        #check up (N)
        if(y > 0):
            if(self.map.isNotWall(y-1, x)): #Wall isn't in the way
                if(self.map.isDoor(y-1, x)): #Locked door, need to kick
                    possibleSteps.append([20, 1, 1])
                possibleSteps.append([1])
                coords.append((y-1, x))
        #check right (E)
        if(x < self.map.getEnviromentDimensions()[1]-1):
            if(self.map.isNotWall(y, x+1)): #Wall isn't in the way
                if(self.map.isDoor(y, x+1)): #Locked door, need to kick
                    possibleSteps.append([20, 2, 2])
                possibleSteps.append([2])
                coords.append((y, x+1))
        #check down (S)
        if(y < self.map.getEnviromentDimensions()[0]-1):
            if(self.map.isNotWall(y+1, x)): #Wall isn't in the way
                if(self.map.isDoor(y+1, x)): #Locked door, need to kick
                    possibleSteps.append([20, 3, 3])
                possibleSteps.append([3])
                coords.append((y+1, x))
        #check left (W)
        if(x > 0):
            if(self.map.isNotWall(y, x-1)): #Wall isn't in the way
                if(self.map.isDoor(y, x-1)): #Locked door, need to kick
                    possibleSteps.append([20, 4, 4])
                possibleSteps.append([4])
                coords.append((y, x-1))
        
        #check up right (NE)
        if(y > 0 and x < self.map.getEnviromentDimensions()[1]-1):
            if(self.map.isNotWall(y-1, x+1, diagonal=True)):
                possibleSteps.append([5])
                coords.append((y-1, x+1))
        #check down right (SE)
        if(y < self.map.getEnviromentDimensions()[0]-1 and x < self.map.getEnviromentDimensions()[1]-1):
            if(self.map.isNotWall(y+1, x+1, True)):
                possibleSteps.append([6])
                coords.append((y+1, x+1))
        #check down left (SW)
        if(y < self.map.getEnviromentDimensions()[0]-1 and x > 0):
            if(self.map.isNotWall(y+1, x-1, True)):
                possibleSteps.append([7])
                coords.append((y+1, x-1))
        #check up left (NW)
        if(y > 0 and x > 0):
            if(self.map.isNotWall(y-1, x-1, True)):
                possibleSteps.append([8])
                coords.append((y-1, x-1))
        return possibleSteps, coords

    def step(self, action):
        if not self.done:
            obs, reward, done, *rest = self.env.step(action)
            self.map.update(obs)
            self.done = done
            blstats = [_ for _ in obs["blstats"]]
            self.score = blstats[9]
            self.moves = blstats[20]
            self.x_pos, self.y_pos = blstats[0], blstats[1]
            self.visited.add((self.y_pos, self.x_pos))

    def render(self):
        self.env.render()

    def buildGraph(self):
        """Builds initial graph"""
        start = time()
        if not (self.x_pos, self.y_pos) in self.graphNodes:
            self.graphNodes[(self.x_pos, self.y_pos)] = GraphNode([], self.x_pos, self.y_pos)
        newNodes = []
        prioQue = []

        # Build queue and find new nodes
        for y in range(self.map.getEnviromentDimensions()[0]):
            for x in range(self.map.getEnviromentDimensions()[1]):
                if (self.map.isDoor(y, x) or self.map.isNewRoute(self, y, x)) and (self.y_pos, self.x_pos) != (y, x):
                    if not (y,x) in self.visited:
                        if not (x,y) in self.graphNodes:
                            newNodes.append((x, y))
                            self.graphNodes[(x,y)] = GraphNode([], x, y)
                        heappush(prioQue, (self.heuristic(self, self.graphNodes[(x,y)]), self.graphNodes[(x,y)]))

        # Remove old current location node
        if len(self.locationStack) > 0:
            ourLocation = self.locationStack[-1]
            if (self.x_pos, self.y_pos) != ourLocation and not self.map.isDoor(ourLocation[1], ourLocation[0]):
                del self.graphNodes[ourLocation]
                for door in self.graphNodes:
                    self.graphNodes[door].removeEdge(ourLocation)

        # Add new current location node edges
        ourLocation = (self.x_pos,self.y_pos)
        if (self.x_pos, self.y_pos) != ourLocation:
            for door in self.graphNodes:
                if door != ourLocation:
                    path = findPathInGridWorld(self.map, ourLocation, door, ignoreDoors=False)
                    if not path is None:
                        self.graphNodes[ourLocation].addEdge(GraphEdge(self.graphNodes[ourLocation], self.graphNodes[door], path))
                        self.graphNodes[door].addEdge(GraphEdge(self.graphNodes[door], self.graphNodes[ourLocation], list(reversed(path))))

        # Add edges to new nodes
        tried = set()
        for i1, door1 in enumerate(newNodes):
            for i2, door2 in enumerate(self.graphNodes):
                cacheKey = tuple(sorted([door1, door2]))
                if door1 != door2:
                    if not cacheKey in tried:
                        tried.add(cacheKey)
                        path = findPathInGridWorld(self.map, door1, door2, ignoreDoors=False)
                        if not path is None:
                            self.graphNodes[door1].addEdge(GraphEdge(self.graphNodes[door1], self.graphNodes[door2], path))
                            self.graphNodes[door2].addEdge(GraphEdge(self.graphNodes[door2], self.graphNodes[door1], list(reversed(path))))
        
        self.pQueue = prioQue
        self.graph = self.graphNodes[(self.x_pos, self.y_pos)]
        self.locationStack.append((self.x_pos, self.y_pos))
        print(f"Graph Build Time: {time()-start}")

    def generalGraphAStar(self, start, target, heuristic):
        queue = []
        # queue = heapify(queue)
        heappush(queue, (0, start))

        cameFrom = {str(start.y)+","+str(start.x): (None, None)}
        costs = {str(start.y)+","+str(start.x): 0}

        while(len(queue) > 0):
            currentNode = heappop(queue)[1]
            if(currentNode == target):
                return self.getPath(start, target, cameFrom)
            for path in currentNode.getEdges():
                possibleCost = costs[str(currentNode.y)+","+str(currentNode.x)] + path.getPathCost()
                to = path.getTo()
                pth = path.getPath()
                try:
                    if(possibleCost < costs[str(to.y)+","+str(to.x)]):
                        costs[str(to.y)+","+str(to.x)] = possibleCost
                        heappush(queue, (possibleCost + path.getPathCost(), to))
                        # queue.heappush((possibleCost + heuristic(to, target), to))
                        cameFrom[str(to.y)+","+str(to.x)] = (currentNode, pth)
                except:
                    costs[str(to.y)+","+str(to.x)] = possibleCost
                    heappush(queue, (possibleCost + path.getPathCost(), to))
                    # queue.heappush((possibleCost + heuristic(to, target), to))
                    cameFrom[str(to.y)+","+str(to.x)] = (currentNode, pth)
        return None

    def getPath(self, start, target, cameFrom):
        path = []
        c_node = target
        while True:
            if(cameFrom[str(c_node.y)+","+str(c_node.x)][0] == None):
                return path
            path = cameFrom[str(c_node.y)+","+str(c_node.x)][1] + path[1:] 
            c_node = cameFrom[str(c_node.y)+","+str(c_node.x)][0]

    def logPath(self, path):    
        for point in path:
            self.heatmap_graph.append_point("heat_pos", point)
    
    def addDoor(self, y,x):
        if(self.map[y][x] == 124 or self.map[y][x] == 45):
            if(self.colors[y][x] == 7): #Checks if not a door
                return False
            else: #add door by calling A* 
                self.map[y][x] = astar.Node((y,x), self.map[y][x], self)

    def findMeanVisiblePositions(self):
        """Finds the mean visited position using floor as a proxy"""
        height, width = self.map.getEnviromentDimensions()
        sumX = 0
        sumY = 0
        count = 0
        for row in range(height):
            for col in range(width):
                if self.map.isNotWall(row, col):
                    count += 1
                    sumX += col 
                    sumY += row 
        return (sumX/count, sumY/count)

    def plotVisited(self):
        height, width = self.map.getEnviromentDimensions()
        axes = plt.axes()
        for y in range(height):
            for x in range(width):
                if (y,x) in self.visited:
                    rect = patches.Rectangle((x,y), 1,1, facecolor='g')
                    axes.add_patch(rect)
                if self.map.isWall(y,x):
                    rect = patches.Rectangle((x,y), 1,1)
                    axes.add_patch(rect)
        plt.show()

if __name__ == "__main__":
    agent = Agent("NetHackScore-v0", furthestDistanceFromMeanAndClosestToUs)

    # Let's try and play
    agent.play()
