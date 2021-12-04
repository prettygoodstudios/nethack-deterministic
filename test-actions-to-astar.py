from Agent import Agent


if __name__ == "__main__":
    agent = Agent("NetHackScore-v0")
    agent.buildGraph()
    if len(agent.graph.getEdges()) > 0:
        print(agent.graph.getEdges()[0].getPath())
        moves = agent.getMoves(agent.graph.getEdges()[0].getPath())
        agent.graph.plot(agent.map)
        print(moves)
        for move in moves:
            for m in move:
                agent.step(m)
        agent.render()
        agent.buildGraph()
        agent.buildGraph()
        agent.graph.plot(agent.map)
    