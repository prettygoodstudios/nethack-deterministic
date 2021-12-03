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


class Agent:
    score = 0
    x_pos = None
    y_pos = None
    env = None
    map = None
    heatmap_graph = None

    def __init__(self, type):
        self.env = gym.make(type)
        obs = self.env.reset()
        self.map = Map(self.env, obs)
        blstats = [_ for _ in obs["blstats"]]
        self.score = blstats[9]
        self.x_pos, self.y_pos = blstats[0], blstats[1]
        self.heatmap_graph = GraphBuilder(["heat_pos"])

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
            if(coords[i][y]-1 == current[y] and coords[i][x]+1 == current[x]):
                steps.append([5])
            elif(coords[i][y]+1 == current[y] and coords[i][x]+1 == current[x]):
                steps.append([6])
            elif(coords[i][y]+1 == current[y] and coords[i][x]-1 == current[x]):
                steps.append([7])
            elif(coords[i][y]-1 == current[y] and coords[i][x]-1 == current[x]):
                steps.append([8])
            elif(coords[i][y]-1 == current[y]):
                if(self.map.isDoor(coords[i][y]-1, coords[i][x])): #Locked door, need to kick
                    steps.append([20, 1, 1])
                else:
                    steps.append([1])
            elif(coords[i][x]+1 == current[x]):
                if(self.map.isDoor(coords[i][y], coords[i][x]+1)): #Locked door, need to kick
                    steps.append([20, 2, 2])
                else:
                    steps.append([2])
            elif(coords[i][y]+1 == current[y]):
                if(self.map.isDoor(coords[i][y]+1, coords[i][x])): #Locked door, need to kick
                    steps.append([20, 3, 3])
                else:
                    steps.append([3])
            elif(coords[i][x]-1 == current[x]):
                if(self.map.isDoor(coords[i][y], coords[i][x]-1)): #Locked door, need to kick
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
        obs = self.env.step(action)
        self.map.update(obs)
        blstats = [_ for _ in obs["blstats"]]
        self.score = blstats[9]
        self.x_pos, self.y_pos = blstats[0], blstats[1]
        self.buildGraph()

    def render(self):
        self.env.render()

    def buildGraph(self):
        """Builds initial graph"""
        doors = [(self.x_pos, self.y_pos)]
        doorLookup = { (self.x_pos, self.y_pos): GraphNode([], self.x_pos, self.y_pos) }
        for y in range(self.map.getEnviromentDimensions()[0]):
            for x in range(self.map.getEnviromentDimensions()[1]):
                if self.map.isDoor(y, x):
                    doors.append((x, y))
                    doorLookup[(x,y)] = GraphNode([], x, y)
        for i1, door1 in enumerate(doors):
            for i2, door2 in enumerate(doors):
                if i1 != i2:
                    path = findPathInGridWorld(self.map, door1, door2, ignoreDoors=False)
                    if not path is None:
                        doorLookup[door1].addEdge(GraphEdge(doorLookup[door1], doorLookup[door2], path))
        self.graph = doorLookup[(self.x_pos, self.y_pos)]

    def generalGraphAStar(self, start, target, heuristic):
        queue = []
        queue = heapify(queue)
        queue.heappush((0, start))

        cameFrom = {start: (None, None)}
        costs = {start: 0}

        while(len(queue) > 0):
            currentNode = queue.heappop()
            if(currentNode == target):
                return self.getPath(start, cameFrom)
            for path in currentNode.getEdges:
                possibleCost = costs[currentNode] + path.getPathCost()
                if(path.__to != currentNode):
                    to = path.__to
                    pth = to.getPath()
                else:
                    to = path.__from
                    pth = reversed(to.getPath())
                try:
                    if(possibleCost < costs[to]):
                        costs[to] = possibleCost
                        queue.heappush((possibleCost + heuristic(to, target), to))
                        cameFrom[to] = (currentNode, pth)
                except:
                    costs[to] = possibleCost
                    queue.heappush((possibleCost + heuristic(to, target), to))
                    cameFrom[to] = (currentNode, pth)
        return None

    def getPath(self, target, cameFrom):
        path = []
        c_node = target
        while True:
            if(cameFrom[c_node][0] == None):
                return path
            path = path + cameFrom[c_node][1]
            c_node = cameFrom[c_node][0]

    def logPath(self, path):
        for point in path:
            self.heatmap_graph.append_point("heat_pos", point)

if __name__ == "__main__":
    agent = Agent("NetHackScore-v0")
    agent.buildGraph()
    print(agent.graph)
    agent.graph.plot()
    

