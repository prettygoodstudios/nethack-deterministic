import sys
sys.path.append("..")
from Agent import Agent
from astar import MockAgent, findPathInGridWorld, renderTestData
from main import MoveActions, Space
from sys import argv

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