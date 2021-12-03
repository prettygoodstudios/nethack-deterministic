from matplotlib import pyplot as plt

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

    def plot(self) -> str:
        """Plots graph using matplotlib"""
        traversedEdges = set()
        def traverse(node: GraphNode):
            nonTraversedEdges = list(filter(lambda x: not str(x) in traversedEdges,node.getEdges()))
            plt.scatter([node.x], [node.y],)
            plt.annotate(f"({node.x},{node.y})", (node.x, node.y))
            if len(nonTraversedEdges) == 0:
                return
            for edge in nonTraversedEdges:
                traversedEdges.add(str(edge))
                plt.plot([node.x, edge.getTo().x], [node.y, edge.getTo().y])
                traverse(edge.getTo())
        traverse(self)
        plt.show()
