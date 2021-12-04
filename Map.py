from utils.graphs import GraphBuilder


class Map:
    map = None
    colors = None
    env = None
    obs = None

    def __init__(self, env, obs):
        self.env = env
        self.obs = obs
        self.colors = obs['colors']
        self.map = obs['chars']

    def isDoor(self, y, x):
        if(self.map[y][x] == 124 or self.map[y][x] == 45):
            if(self.colors[y][x] != 7): #Checks if not a door
                return True
        if(self.map[y][x] == 43):
            return True
        return False
    
    def isInRoom(self, y, x):
        if(self.map[y][x] == 46):
            return True
        return False

    def getEnviromentDimensions(self):
        return (len(self.map), len(self.map[0]))

    def isNotWall(self, y, x, diagonal=False): #Treats boulders as walls
        if(self.map[y][x] == 96 or self.map[y][x] == 32):
            return False
        if(self.map[y][x] == 124 or self.map[y][x] == 45):
            if(self.colors[y][x] == 7): #Checks if not a door
                return False
            elif(diagonal): #Cannot move diagonally into doorways
                return False
        return True

    def isWall(self, y, x, diagonal=False):
        return not self.isNotWall(y, x, diagonal)

    def update(self, obs):
        self.obs = obs


    