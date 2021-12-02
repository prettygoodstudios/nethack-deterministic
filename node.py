#based on what do we get to a spicific node
# which class it should be defined in
# do you need any output
class GraphEdge():
    def __init__(self, __from, __to,__path):
        self.__from = __from
        self.__to = __to
        self.__path = __path
    def getPath(self):
        print(self.__path)
        return self.__path
    def getPathCost(self):
        return len(self.__path)
    def getPaths(self):
        return self.__path

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
