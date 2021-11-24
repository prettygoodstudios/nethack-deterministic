# change it to a list so we can store the path in the vertex
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
    def getPatCost(self):
        return len(self.__path)

    # def getNode(self, node):
    #     if node in self.__path:


""" these are the doors """
class GraphNode():
    def __init__(self, __edges):
        self.__edges = __edges

    def addEdge(self,__edge):
        self.__edges.append(__edge)
    def getEdges(self):
        return self.__edges
