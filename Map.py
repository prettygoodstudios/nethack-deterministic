from utils.graphs import GraphBuilder


class Map:
    map = None
    colors = None
    env = None
    obs = None
    doors = set()

    def __init__(self, env, obs):
        self.env = env
        self.obs = obs
        self.colors = obs['colors']
        self.map = obs['chars']
        
    def isNewRoute(self, a, y, x):
        y_bound = self.getEnviromentDimensions()[0]-1
        x_bound = self.getEnviromentDimensions()[1]-1
        if (y, x) in a.visited or self.isWall(y,x):
            return False
        isNew = False
        if y > 0:
            isNew = isNew or self.map[y-1][x] == 32
        if y < y_bound:
            isNew = isNew or self.map[y-1][x] == 32
        if x > 0:
            isNew = isNew or self.map[y][x-1] == 32
        if x < x_bound:
            isNew = isNew or self.map[y][x+1] == 32
        if y > 0 and x > 0:
            isNew = isNew or self.map[y-1][x-1] == 32
        if y > 0 and x < x_bound:
            isNew = isNew or self.map[y-1][x+1] == 32
        if y < y_bound and x < x_bound:
            isNew = isNew or self.map[y+1][x+1] == 32
        if y < y_bound and x > 0:
            isNew = isNew or self.map[y+1][x-1] == 32
        return isNew
            #if(y == 0 and x == 0):
            #    return (self.map[y+1][x] != 32 or self.map[y][x+1] != 32 or self.map[y+1][x+1] != 32)
            #elif(y == y_bound and x == x_bound):
            #    return (self.map[y-1][x-1] != 32 or self.map[y][x-1] != 32 or self.map[y-1][x] != 32)
            #elif(y == 0):
            #    return (self.map[y+1][x] != 32 or self.map[y][x+1] != 32 or self.map[y+1][x+1] != 32 or self.map[y+1][x-1] != 32 or self.map[y][x-1] != 32)
            #elif(x == 0):
            #    return (self.map[y][x+1] != 32 or self.map[y+1][x] != 32 or self.map[y+1][x+1] != 32 or self.map[y-1][x+1] != 32 or self.map[y-1][x] != 32)
            #elif(y == y_bound):
            #    return (self.map[y-1][x-1] != 32 or self.map[y][x-1] != 32 or self.map[y-1][x] != 32 or self.map[y-1][x+1] != 32 or self.map[y][x+1] != 32)
            #elif(x == x_bound):
            #    return (self.map[y-1][x-1] != 32 or self.map[y][x-1] != 32 or self.map[y+1][x-1] != 32 or self.map[y-1][x] != 32 or self.map[y+1][x] != 32)
            #return (self.map[y-1][x-1] != 32 or self.map[y][x-1] != 32 or self.map[y+1][x-1] != 32 or self.map[y-1][x] != 32 or self.map[y+1][x] != 32 or self.map[y-1][x+1] != 32 or self.map[y][x+1] != 32 or self.map[y+1][x+1] != 32)
        

    def isDoor(self, y, x):
        if (y,x) in self.doors:
            return True
        if(self.map[y][x] == 124 or self.map[y][x] == 45):
            if(self.colors[y][x] != 7): #Checks if not a door
                return True
        if(self.map[y][x] == 43):
            return True
        if(y > 0 and y < self.getEnviromentDimensions()[0]-1) and x > 0 and x < self.getEnviromentDimensions()[1]-1:
            if(self.map[y][x] != 124 or self.map[y][x] != 45):
                if((self.map[y-1][x] == 124 or self.map[y-1][x] == 45) and (self.map[y+1][x] == 124 or self.map[y+1][x] == 45) and (self.map[y][x-1] == 32 or self.map[y][x+1] == 32) and self.isNotWall(y, x)):
                    return True
                elif((self.map[y][x-1] == 124 or self.map[y][x-1] == 45) and (self.map[y][x+1] == 124 or self.map[y][x+1] == 45) and (self.map[y-1][x] == 32 or self.map[y+1][x] == 32) and self.isNotWall(y, x)):
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
        self.__updateDoors()

    def findStairs(self):
        y_bound, x_bound = self.map.shape
        for y in range(y_bound):
            for x in range(x_bound):
                if(self.map[y][x] == 62):
                    return (y, x)
        return None

    def __updateDoors(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                if self.isDoor(y,x):
                    self.doors.add((y,x))



    
