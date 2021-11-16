from heapq import heappush, heappop
from enum import Enum
from functools import reduce
import nle
import gym
from numpy import sqrt

class MoveActions(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    UP_RIGHT = 5
    DOWN_RIGHT = 6
    DOWN_LEFT = 7
    UP_LEFT = 8

class NonMoveActions(Enum):
    SEARCH = 22

class Space(Enum):
    HORIZONTAL_WALL = 2361
    VERTICAL_WALL = 2360
    EMPTYNESS = 2359
    OPEN_DOOR = 2374

class Node:
    """Node used by A* algo"""
    __position: tuple
    __cost: float

    def __init__(self, position: tuple, cost: float, parent) -> None:
        self.__position = position 
        self.__cost = cost
        self.__parent = parent

    def updateCost(self, cost, parent) -> None:
        if cost < self.__cost:
            self.__cost = cost 
            self.__parent = parent

    def getCost(self) -> float:
        return self.__cost

    def getPosition(self) -> tuple:
        return self.__position

    def getParent(self):
        return self.__parent

    def __lt__(self, other):
        """Comparision uses cost"""
        return self.getCost() < other.getCost()

    def __eq__(self, o: object) -> bool:
        return self.__position == o.getPosition()
    
    def __hash__(self) -> int:
        return hash(self.__position)


def computeMove(env, visited):
    """Computes Move"""
    actionDirection = {
        MoveActions.UP: (0, -1),
        MoveActions.DOWN: (0, 1),
        MoveActions.LEFT: (-1, 0),
        MoveActions.RIGHT: (1, 0),
        MoveActions.UP_RIGHT: (1, -1),
        MoveActions.DOWN_LEFT: (-1, 1),
        MoveActions.DOWN_RIGHT: (1, 1),
        MoveActions.UP_LEFT: (-1, -1)
    }
    directionToAction = {}
    for k in actionDirection:
        directionToAction[actionDirection[k]] = k
    state, reward, _, _ = env.step(MoveActions.UP.value)
    x, y, *rest = state['blstats']
    walls = set((Space.HORIZONTAL_WALL.value, Space.VERTICAL_WALL.value))
    cannotMove = set((Space.HORIZONTAL_WALL.value, Space.VERTICAL_WALL.value, Space.EMPTYNESS.value))
    exits = set()
    for ri, row in enumerate(state['glyphs'][1:-1]):
        for ci, col in enumerate(row[1:-1]):
            if not col in cannotMove:
                if state['glyphs'][ri-1][ci] in walls and state['glyphs'][ri+1][ci] in walls:
                    exits.add((ci, ri))

    openSet = {(x, y): Node((x, y), 0, None)}
    openQueue = [openSet[k] for k in openSet]
    closedSet = {}
    while len(openSet) > 0:            
        current = heappop(openQueue)
        openSet.pop(current.getPosition())
        currX, currY = current.getPosition()
        closedSet[current.getPosition()] = current
        # Ensure in bounds
        for action in MoveActions:
            newX, newY = actionDirection[action][0] + currX, actionDirection[action][1] + currY
            if not (newX, newY) in closedSet:
                inBounds = newY < len(state['glyphs']) and newX < len(state['glyphs'][0]) and newX >= 0 and newY >= 0
                if inBounds and not state['glyphs'][newY][newX] in cannotMove:
                    if (newX, newY) in openSet:
                        openSet[(newX, newY)].updateCost(current.getCost() + 1, current)
                    else:
                        openSet[(newX, newY)] = Node((newX, newY), current.getCost() +1, current)
                        heappush(openQueue, openSet[(newX, newY)])
    meanPosition = (sum([v[0] for v in visited])/len(visited), sum([v[1] for v in visited])/len(visited))
    furthest = max([closedSet[k] for k in closedSet], key=lambda n: (n.getPosition()[0] - meanPosition[0]) ** 2 + (n.getPosition()[1] - meanPosition[1]) ** 2)
    for k in closedSet:
        if closedSet[k].getPosition() in exits:
            furthest = closedSet[k]
    path = []
    while not furthest is None:
        path.append(furthest)
        furthest = furthest.getParent()
    path.reverse()
    actions = []
    for move in path[1:]:
        mX, mY = move.getPosition()
        actions.append(directionToAction[(mX - x, mY - y)])
        x = mX 
        y = mY
    return actions



if __name__ == "__main__":
    env = gym.make("NetHackScore-v0")
    env.reset()
    state, reward, _, _ = env.step(MoveActions.UP.value)
    x, y, *rest = state['blstats']
    visited = set()
    visited.add((x, y))
    for _ in range(10):
        for action in computeMove(env, visited):
            state, reward, _, _ = env.step(action.value)
            x, y, *rest = state['blstats']
            visited.add((x, y))
        env.step(NonMoveActions.SEARCH.value)
        env.render()

    # env.actions to get set of actions
    print(visited)
