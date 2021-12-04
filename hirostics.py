import node
import Agent
import math


def queueBased(self, Agent a, node n):
    self.cost = 0
    sum = Agent.findmeanVistiedPostion()
    pNode = [n.x, ny]
    pAgent = [sum.x_pos, sum.y_pos]
    self.distance = math.sqrt( ((pNode[0]-pAgent[0])**2)+((pNode[1]-pAgent[1])**2) )
    if self.cost < self.distance:
        self.cost = self.distance
        #return self.cost
    return self.cost