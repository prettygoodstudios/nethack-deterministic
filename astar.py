import nle
import gym

from heapq import heappop, heappush
from main import MoveActions, Space




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


def findPathInGridWorld(map: list, start: tuple, goal: tuple):
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
    cannotMove = set((Space.HORIZONTAL_WALL.value, Space.VERTICAL_WALL.value, Space.EMPTYNESS.value))
    openSet = {start: Node(start, 0, None)}
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
            if (newX, newY) == goal:
                path = [(newX, newY)]
                while not current is None:
                    path.append(current.getPosition())
                    current = current.getParent()
                return list(reversed(path))
            if not (newX, newY) in closedSet:
                inBounds = newY < len(map) and newX < len(map[0]) and newX >= 0 and newY >= 0
                if inBounds and not map[newY][newX] in cannotMove:
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

if __name__ == "__main__":
    #env = gym.make("NetHackScore-v0")
    #env.reset()
    #env.render()
    #state, reward, _, _ = env.step(MoveActions.UP.value)
    #x, y, *rest = state['blstats']
    #print((x, y))
    #print(findPathInGridWorld(state['glyphs'], (x,y), (x+5, y+5)))
    
    # Tests for A* 
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
        
    renderTestData(testData1, set(findPathInGridWorld(testData1, (1, 8), (8, 8))))
    renderTestData(testData1, set(findPathInGridWorld(testData1, (1, 1), (8, 8))))
    renderTestData(testData1, set(findPathInGridWorld(testData1, (2, 5), (8, 8))))

    testData2 = [
        [Space.HORIZONTAL_WALL.value for _ in range(10)],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(8)] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0, 0] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0, 0] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(3)] + [Space.VERTICAL_WALL.value] + [0, Space.VERTICAL_WALL.value] + [Space.VERTICAL_WALL.value] + [0] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
        [Space.VERTICAL_WALL.value] + [0 for _ in range(5)] + [Space.VERTICAL_WALL.value] + [0 for _ in range(2)] + [Space.VERTICAL_WALL.value],
        [Space.HORIZONTAL_WALL.value for _ in range(10)],
    ]

    renderTestData(testData2, set(findPathInGridWorld(testData2, (1, 8), (8, 8))))
    renderTestData(testData2, set(findPathInGridWorld(testData2, (1, 1), (8, 8))))
    renderTestData(testData2, set(findPathInGridWorld(testData2, (2, 5), (8, 8))))
    