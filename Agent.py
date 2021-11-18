import gym
from gym.spaces.box import Box
import nle
from nle import nethack as nh
import time
import numpy as np
from heapq import heapify, heappush, heappop
from dataclasses import dataclass, field
from typing import Any


class Agent:
    map = None
    colors = None
    score = 0
    x_pos = None
    y_pos = None
    env = None

    def __init__(self, type):
        self.env = gym.make(type)
        obs = self.env.reset()
        self.colors = obs['colors']
        self.map = obs['chars']
        blstats = [_ for _ in obs["blstats"]]
        self.score = blstats[9]
        self.x_pos, self.y_pos = blstats[0], blstats[1]

    def isDoor(self, y, x):
        if(self.map[y][x] == 124 or self.map[y][x] == 45):
            if(self.colors[y][x] != 7): #Checks if not a door
                return True
        if(self.map[y][x] == 43):
            return True
        return False

    def isNotWall(self, y, x, diagonal=False): #Treats boulders as walls
        if(self.map[y][x] == 96):
            return False
        if(self.map[y][x] == 124 or self.map[y][x] == 45):
            if(self.colors[y][x] == 7): #Checks if not a door
                return False
            elif(diagonal): #Cannot move diagonally into doorways
                return False
        return True

    def isWall(self, y, x, diagonal=False):
        return not self.isNotWall(y, x, diagonal)

    def getPossibleMoves(self, y, x):
        possibleSteps = []
        coords = []
        #check up (N)
        if(y > 0):
            if(self.isNotWall(y-1, x)): #Wall isn't in the way
                if(self.map[y-1][x] == 43): #Locked door, need to kick
                    possibleSteps.append([20, 1, 1])
                possibleSteps.append([1])
                coords.append((y-1, x))
        #check right (E)
        if(x < len(self.map[0])-1):
            if(self.isNotWall(y, x+1)): #Wall isn't in the way
                if(self.map[y][x+1] == 43): #Locked door, need to kick
                    possibleSteps.append([20, 2, 2])
                possibleSteps.append([2])
                coords.append((y, x+1))
        #check down (S)
        if(y < len(self.map)-1):
            if(self.isNotWall(y+1, x)): #Wall isn't in the way
                if(self.map[y+1][x] == 43): #Locked door, need to kick
                    possibleSteps.append([20, 3, 3])
                possibleSteps.append([3])
                coords.append((y+1, x))
        #check left (W)
        if(x > 0):
            if(self.isNotWall(y, x-1)): #Wall isn't in the way
                if(self.map[y][x-1] == 43): #Locked door, need to kick
                    possibleSteps.append([20, 4, 4])
                possibleSteps.append([4])
                coords.append((y, x-1))
        
        #check up right (NE)
        if(y > 0 and x < len(self.map[0])-1):
            if(self.isNotWall(y-1, x+1, diagonal=True)):
                possibleSteps.append([5])
                coords.append((y-1, x+1))
        #check down right (SE)
        if(y < len(self.map)-1 and x < len(self.map[0])-1):
            if(self.isNotWall(y+1, x+1, True)):
                possibleSteps.append([6])
                coords.append((y+1, x+1))
        #check down left (SW)
        if(y < len(self.map)-1 and x > 0):
            if(self.isNotWall(y+1, x-1, True)):
                possibleSteps.append([7])
                coords.append((y+1, x-1))
        #check up left (NW)
        if(y > 0 and x > 0):
            if(self.isNotWall(y-1, x-1, True)):
                possibleSteps.append([8])
                coords.append((y-1, x-1))
        return possibleSteps, coords

    def step(self, action):
        obs = self.env.step(action)
        self.colors = obs['colors']
        self.map = obs['chars']
        blstats = [_ for _ in obs["blstats"]]
        self.score = blstats[9]
        self.x_pos, self.y_pos = blstats[0], blstats[1]

    def render(self):
        self.env.render()