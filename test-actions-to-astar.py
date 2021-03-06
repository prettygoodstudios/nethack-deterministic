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
            startX, startY = agent.getX(), agent.getY()
            while True:
                for m in move:
                    agent.step(m)
                if (startX, startY) != (agent.getX(), agent.getY()):
                    break
        agent.render()
        agent.buildGraph()
        agent.graph.plot(agent.map) 
        
    