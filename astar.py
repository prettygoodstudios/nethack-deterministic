import nle
import gym

from abc import ABC, abstractmethod
from heapq import heappop, heappush
from main import MoveActions, Space
from Agent import Agent
from sys import argv




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

    def __repr__(self) -> str:
        return str(self.__position)

class PathFindingAgent(ABC):
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
    def getPossibleMoves(self, y, x) -> tuple:
        """Returns possible moves first element action number, second element coordinate"""

    @abstractmethod
    def getEnviromentDimensions(self) -> tuple:
        """Returns dimensions of enviroment"""

    @abstractmethod
    def getX(self) -> int:
        """Gets x position of agent"""

    @abstractmethod 
    def getY(self) -> int:
        """Gets y position of agent"""


def findPathInGridWorld(agent: PathFindingAgent, start: tuple, goal: tuple, ignoreDoors=True):
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
    openSet = {start: Node(start, 0, None)}
    openQueue = [openSet[k] for k in openSet]
    closedSet = {}
    height, width = agent.getEnviromentDimensions()
    while len(openSet) > 0:
        current = heappop(openQueue)
        openSet.pop(current.getPosition())
        currX, currY = current.getPosition()
        closedSet[current.getPosition()] = current
        # Ensure in bounds
        for action in MoveActions:
            newX, newY = actionDirection[action][0] + currX, actionDirection[action][1] + currY
            if (newX, newY) == goal:
                path = [(newX, newY)]
                while not current is None:
                    path.append(current.getPosition())
                    current = current.getParent()
                return list(reversed(path))
            if not (newX, newY) in closedSet:
                inBounds = newY < height and newX < width and newX >= 0 and newY >= 0
                isNotWall = agent.isNotWall(newY, newX, diagonal=(newX != currX and newY != currY))
                if inBounds and isNotWall and ( ignoreDoors or not agent.isDoor(newY, newX) ):
                    if (newX, newY) in openSet:
                        openSet[(newX, newY)].updateCost(current.getCost() + 1, current)
                    else:
                        openSet[(newX, newY)] = Node((newX, newY), current.getCost() +1, current)
                        heappush(openQueue, openSet[(newX, newY)])
    return None

def renderTestData(data: list, path: set = set()) -> None:
    """Simply used for debugging"""
    cannotMove = set((Space.HORIZONTAL_WALL.value, Space.VERTICAL_WALL.value, Space.EMPTYNESS.value))
    for ri, row in enumerate(data):
        for vi, value in enumerate(row):
            if (vi, ri) in path:
                print('*', end='')
            elif value in cannotMove:
                print('x', end='')
            else:
                print(' ', end='')
        print()



class MockAgent(PathFindingAgent):
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

    def getY(self) -> int:
        return 0

    def getX(self) -> int:
        return 0

if __name__ == "__main__":
    #env = gym.make("NetHackScore-v0")
    #env.reset()
    #env.render()
    #state, reward, _, _ = env.step(MoveActions.UP.value)
    #x, y, *rest = state['blstats']
    #print((x, y))
    #print(findPathInGridWorld(state['glyphs'], (x,y), (x+5, y+5)))
    
    
    if '-t' in argv:
        # Tests for A* will run tests if -t argument provided
        
        testData1 = [
            [Space.HORIZONTAL_WALL.value for _ in range(10)],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(4)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0, 0] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0, 0] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
            [Space.HORIZONTAL_WALL.value for _ in range(10)],
        ]
        mockOne = MockAgent(testData1)   
        renderTestData(testData1, set(findPathInGridWorld(mockOne, (1, 8), (8, 8))))
        renderTestData(testData1, set(findPathInGridWorld(mockOne, (1, 1), (8, 8))))
        renderTestData(testData1, set(findPathInGridWorld(mockOne, (2, 5), (8, 8))))

        testData2 = [
            [Space.HORIZONTAL_WALL.value for _ in range(10)],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0, 0] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0, 0] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [Space.OPEN_DOOR.value, Space.VERTICAL_WALL.value] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
            [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
            [Space.HORIZONTAL_WALL.value for _ in range(10)],
        ]
        mockTwo = MockAgent(testData2)  

        renderTestData(testData2, set(findPathInGridWorld(mockTwo, (1, 8), (8, 8))))
        renderTestData(testData2, set(findPathInGridWorld(mockTwo, (1, 1), (8, 8))))
        renderTestData(testData2, set(findPathInGridWorld(mockTwo, (2, 5), (8, 8))))
    else:
        # If test flag not provided run with actual agent
        agent = Agent("NetHackScore-v0")
        result = findPathInGridWorld(agent, (agent.getX(), agent.getY()), (8, 8))
        agent.logPath(result)
        agent.heatmap_graph.save_graphs()
        print(result)
        agent.render()