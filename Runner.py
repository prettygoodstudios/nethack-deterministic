from Agent import Agent
import Map

agent = Agent("NetHackScore-v0")
nodes = agent.buildGraph()
# print(agent.graph)
# agent.env.render()
# agent.graph.plot(agent.map)
Done = False
# while(not Done):
    # queue = makePriorityQueue(nodes)
    # moves = agent.generalGraphAStar()

# print(agent.getAction)
start = agent.graph
print(type(start))
target = agent.graph.edges[0]._GraphEdge__to
a = agent.generalGraphAStar(start, target, None)
print(a)