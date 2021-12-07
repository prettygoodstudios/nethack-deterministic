from matplotlib import pyplot as plt
from matplotlib import patches

from astar import PathFindingMap

#based on what do we get to a spicific node
# which class it should be defined in
# do you need any output
class GraphEdge():
    def __init__(self, __from, __to,__path):
        self.__from = __from
        self.__to = __to
        self.__path = __path
    def getPath(self):
        return self.__path
    def getPathCost(self):
        return len(self.__path)
    def getPaths(self):
        return self.__path
    def __str__(self) -> str:
        return f"({self.__from.x},{self.__from.y})->({self.__to.x},{self.__to.y})"
    def getTo(self):
        return self.__to

    # def getNode(self, node):
    #     if node in self.__path:



class GraphNode():
    """ these are the doors """
    def __init__(self, edges, x, y):
        self.edges = edges
        self.x = x 
        self.y = y

    def addEdge(self, edge):
        self.edges.append(edge)
    def getEdges(self):
        return self.edges

    def __str__(self) -> str:
        """Traverses graph generating representation"""
        traversedEdges = set()
        def traverse(node: GraphNode):
            nonTraversedEdges = list(filter(lambda x: not str(x) in traversedEdges,node.getEdges()))
            if len(nonTraversedEdges) == 0:
                return ""
            output = ""
            for edge in nonTraversedEdges:
                if not str(edge) in traversedEdges:
                    traversedEdges.add(str(edge))
                    output += f"({node.x},{node.y}) - {edge.getPathCost()} -> ({edge.getTo().x},{edge.getTo().y})\n" 
                    output += traverse(edge.getTo())
            return output 
        return traverse(self)

    def __repr__(self) -> str:
        return str(self)

    def __lt__(self, other):
        return True

    def plot(self, map: PathFindingMap, agent) -> str:
        """Plots graph using matplotlib"""
        traversedEdges = set()
        yVals = range(0, map.getEnviromentDimensions()[0])
        xVals = range(0, map.getEnviromentDimensions()[1])
        #plt.yticks(yVals)
        #plt.xticks(xVals[::5])

        # Draw the walls
        axes = plt.axes()
        for y in yVals:
            for x in xVals:
                if map.isWall(y,x):
                    rect = patches.Rectangle((x,y), 1,1)
                    axes.add_patch(rect)
                if map.isDoor(y,x):
                    rect = patches.Rectangle((x,y), 1,1, facecolor='r')
                    axes.add_patch(rect)
                if map.isNewRoute(agent, y,x):
                    rect = patches.Rectangle((x,y), 1,1, facecolor='r')
                    axes.add_patch(rect)

        # Traverse and draw the nodes and edges
        def traverse(node: GraphNode):
            nonTraversedEdges = list(filter(lambda x: not str(x) in traversedEdges,node.getEdges()))
            plt.scatter([node.x + 0.5], [node.y + 0.5])
            plt.annotate(f"({node.x},{node.y})", (node.x, node.y))
            if len(nonTraversedEdges) == 0:
                return
            for edge in nonTraversedEdges:
                traversedEdges.add(str(edge))
                xPts = [x + 0.5 for y,x in edge.getPath()]
                yPts = [y + 0.5 for y,x in edge.getPath()]
                s = [10 for _ in edge.getPath()]
                plt.scatter(xPts, yPts, s)
                plt.plot(xPts, yPts)
                traverse(edge.getTo())
        traverse(self)
        plt.axis('scaled')
        plt.show()
