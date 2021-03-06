
from abc import ABC, abstractmethod
from heapq import heappop, heappush
from Map import Map
from main import MoveActions, Space


class Node:
    """Node used by A* algo"""
    __position: tuple
    __cost: float

    def __init__(self, position: tuple, goal: tuple, cost: float, parent) -> None:
        self.__position = position 
        self.__cost = cost
        self.__parent = parent
        self.__goal = goal

    def updateCost(self, cost, parent) -> None:
        if cost < self.__cost:
            self.__cost = cost 
            self.__parent = parent

    def getCost(self) -> float:
        return self.__cost + ((self.__position[0] - self.__goal[0]) ** 2 + (self.__position[1] - self.__goal[1]) ** 2) ** 0.5

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

    def __repr__(self) -> str:
        return str(self.__position)

class PathFindingMap(ABC):
    """Abstract class for agents A* is compatible with"""

    @abstractmethod
    def isDoor(self, y, x) -> bool:
        """Returns true if grid cell is door"""

    @abstractmethod 
    def isNotWall(self, y, x, diagonal=False) -> bool:
        """Returns true if cell not wall"""

    @abstractmethod
    def isWall(self, y, x, diagonal=False) -> bool:
        """Returns true if cell is wall"""

    @abstractmethod
    def getEnviromentDimensions(self) -> tuple:
        """Returns dimensions of enviroment"""

def floodSearchInGridWorld(map: Map, start: tuple, ignoreDoors=True) -> dict:
    """Flood search algorithm for nle grid world"""
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
    openSet = {start: Node(start, start, 0, None)}
    openQueue = [openSet[k] for k in openSet]
    closedSet = {}
    height, width = map.getEnviromentDimensions()
    while len(openSet) > 0:
        current = heappop(openQueue)
        openSet.pop(current.getPosition())
        currX, currY = current.getPosition()
        closedSet[current.getPosition()] = current
        # Ensure in bounds
        for action in MoveActions:
            newX, newY = actionDirection[action][0] + currX, actionDirection[action][1] + currY
            diagonal = (newX != currX and newY != currY)
            # Check if legal move
            if not (newX, newY) in closedSet and not (map.isDoor(currY, currX) and diagonal) and not (map.isDoor(newY, newX) and diagonal):
                inBounds = newY < height and newX < width and newX >= 0 and newY >= 0
                isNotWall = map.isNotWall(newY, newX, diagonal=diagonal)
                if inBounds and isNotWall and ( ignoreDoors or not map.isDoor(newY, newX) ):
                    if (newX, newY) in openSet:
                        openSet[(newX, newY)].updateCost(current.getCost() + 1, current)
                    else:
                        openSet[(newX, newY)] = Node((newX, newY), (newX, newY), current.getCost() +1, current)
                        heappush(openQueue, openSet[(newX, newY)])
                elif map.isDoor(newY, newX):
                    if not (newX, newY) in closedSet:
                        closedSet[newX, newY] = Node((newX, newY), (newX, newY), current.getCost() +1, current)
                    else:
                        closedSet[newX, newY].updateCost(current.getCost() + 1, current)
    return closedSet

def findPathUsingFloodSearch(closedSet: dict, goal: tuple) -> list:
    """Uses the closed to find path if exists"""
    if not goal in closedSet:
        # If the goal is not in the closed set then no path exists
        return None
    path = []
    current = closedSet[goal]
    while not current is None:
        path.append(tuple(reversed(current.getPosition())))
        current = current.getParent()
    return list(reversed(path))



def findPathInGridWorld(map: Map, start: tuple, goal: tuple, ignoreDoors=True):
    """A* algorithm for nle grid world"""
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
    openSet = {start: Node(start, goal, 0, None)}
    openQueue = [openSet[k] for k in openSet]
    closedSet = {}
    height, width = map.getEnviromentDimensions()
    while len(openSet) > 0:
        current = heappop(openQueue)
        openSet.pop(current.getPosition())
        currX, currY = current.getPosition()
        closedSet[current.getPosition()] = current
        # Ensure in bounds
        for action in MoveActions:
            newX, newY = actionDirection[action][0] + currX, actionDirection[action][1] + currY
            diagonal = (newX != currX and newY != currY)
            # Check if legal move
            if not (newX, newY) in closedSet and not (map.isDoor(currY, currX) and diagonal) and not (map.isDoor(newY, newX) and diagonal):
                if (newX, newY) == goal:
                    path = [(newY, newX)]
                    while not current is None:
                        path.append(tuple(reversed(current.getPosition())))
                        current = current.getParent()
                    return list(reversed(path))
                inBounds = newY < height and newX < width and newX >= 0 and newY >= 0
                isNotWall = map.isNotWall(newY, newX, diagonal=diagonal)
                if inBounds and isNotWall and ( ignoreDoors or not map.isDoor(newY, newX) ):
                    if (newX, newY) in openSet:
                        openSet[(newX, newY)].updateCost(current.getCost() + 1, current)
                    else:
                        openSet[(newX, newY)] = Node((newX, newY), goal, current.getCost() +1, current)
                        heappush(openQueue, openSet[(newX, newY)])
    return None

def renderTestData(data: list, path: set = set()) -> None:
    """Simply used for debugging"""
    cannotMove = set((Space.HORIZONTAL_WALL.value, Space.VERTICAL_WALL.value, Space.EMPTYNESS.value))
    for ri, row in enumerate(data):
        for vi, value in enumerate(row):
            if (ri, vi) in path:
                print('*', end='')
            elif value in cannotMove:
                print('x', end='')
            else:
                print(' ', end='')
        print()



class MockMap(PathFindingMap):
    """Mocks the agent for testing purposes"""
    __cannotMove = set((Space.HORIZONTAL_WALL.value, Space.VERTICAL_WALL.value, Space.EMPTYNESS.value))
    __glyphs: list = None

    def __init__(self, glyphs: list) -> None:
        self.__glyphs = glyphs

    def isDoor(self, y, x) -> bool:
        """There are no doors in mock data yet"""
        return self.__glyphs[y][x] == Space.OPEN_DOOR.value 

    def isNotWall(self, y, x, diagonal=False) -> bool:
        return not self.__glyphs[y][x] in self.__cannotMove and (not diagonal or self.__glyphs[y][x] != Space.OPEN_DOOR.value)

    def isWall(self, y, x, diagonal=False) -> bool:
        return self.__glyphs[y][x] in self.__cannotMove or (diagonal and self.__glyphs[y][x] == Space.OPEN_DOOR.value)

    def getPossibleMoves(self, y, x) -> tuple:
        """A* algo is not using actions only coords"""
        coords = []
        for row in range(max(y-1, 0), min(y+1, len(self.__glyphs))):
            for col in range(max(x-1, 0), min(x+1, len(self.__glyphs[0]))):
                if self.isNotWall(y, x) and (row, col) != (y, x):
                    coords.append((y, x))
        return [], coords

    def getEnviromentDimensions(self) -> tuple:
        return (len(self.__glyphs), len(self.__glyphs[0]))

