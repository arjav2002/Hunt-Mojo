import pygame
import random
from Room import*
from Sprites import*

display_width_grids = 16
display_height_grids = 10

right_door = (15, 5)
left_door = (0, 5)
top_door = (8, 0)
bottom_door = (8, 9)

class Level():

    def __init__(self, lvl):
        self.lvl = lvl
        self.noOfRooms = 2*lvl+4
        self.roomConnections = [[[]for i in range(3)] for j in range(self.noOfRooms-1)]
        self.rooms = [[]for i in range(self.noOfRooms)]

    def generate(self):       
        last = -1
        def opp(dir):
            if dir == 0:
                return 2
            if dir == 2:
                return 0
            if dir == 1:
                return 3
            if dir == 3:
                return 1
                
        for i in range(self.noOfRooms-1):
            direction = random.randrange(0,4)
            while(last == opp(direction)): direction = random.randrange(0, 4)
            if(direction == 0):
                self.roomConnections[i] = [i,i+1,0] # 0 -> bottom to top    1 -> left to right
            elif(direction == 1):
                self.roomConnections[i] = [i,i+1,1]
            elif(direction == 2):
                self.roomConnections[i] = [i+1,i,0]
            elif(direction == 3):
                self.roomConnections[i] = [i+1,i,1]
            last = direction

        for i in range(self.noOfRooms):
            self.rooms[i] = Room(i,random.randrange(0,len(RoomTypes)),self.lvl)
            self.rooms[i].generate()
    
    def getLeftRoomNo(self, refRoomNo):
        for roomConnection in self.roomConnections:
            if roomConnection[1] == refRoomNo and roomConnection[2] == 1: return roomConnection[0]
        return -1

    def getRightRoomNo(self, refRoomNo):
        for roomConnection in self.roomConnections:
            if roomConnection[0] == refRoomNo and roomConnection[2] == 1: return roomConnection[1]
        return -1
    
    def getTopRoomNo(self, refRoomNo):
        for roomConnection in self.roomConnections:
            if roomConnection[1] == refRoomNo and roomConnection[2] == 0: return roomConnection[0]
        return -1

    def getBottomRoomNo(self, refRoomNo):
        for roomConnection in self.roomConnections:
            if roomConnection[0] == refRoomNo and roomConnection[2] == 0: return roomConnection[1]
        return -1

    def isDoorOperational(self, roomNo, door):
        if(int(door.x/grid_size) == right_door[0] and int(door.y/grid_size) == right_door[1]):
            return self.getRightRoomNo(roomNo) != -1
        elif(int(door.x/grid_size) == left_door[0] and int(door.y/grid_size) == left_door[1]):
            return self.getLeftRoomNo(roomNo) != -1
        elif(int(door.x/grid_size) == top_door[0] and int(door.y/grid_size) == top_door[1]):
            return self.getTopRoomNo(roomNo) != -1
        elif(int(door.x/grid_size) == bottom_door[0] and int(door.y/grid_size) == bottom_door[1]):
            return self.getBottomRoomNo(roomNo) != -1


class Room():

    def __init__(self, no, Rtype, lvl):
        self.no = no
        self.wallGrid = [[[] for i in range(display_width_grids)] for i in range(display_height_grids)]
        self.creatureGrid = [[-1 for i in range(display_width_grids)] for i in range(display_height_grids)]
        self.Rtype = Rtype
        self.noOfSprites = [0 for i in range(4)]
        self.lvl = lvl

    def addSpritesToGrid(self,number,id):
        actualAdded = 0
        for a in range(number):
            i = random.randrange(0,display_width_grids)
            j = random.randrange(0,display_height_grids)

            if(self.wallGrid[j][i] == WallIds.floor.value and self.creatureGrid[j][i] == CreatureIds.noCreature.value):
                self.creatureGrid[j][i] = id
                actualAdded += 1
        
        self.noOfSprites[id] = actualAdded
    

    def generate(self):
        self.wallGrid = RoomTypes[self.Rtype]

        #generating number of sprites of each type

        self.noOfSprites[0] = 1

        for a in range(1,4):
            self.noOfSprites[a] = random.randrange(0,self.lvl+3)

        #adding to grid

        for i in range(1,4):
            self.addSpritesToGrid(self.noOfSprites[i],i)
    
    def areDoorsUnlocked(self):
        flag = True
        # have to ignore player sprite
        for i in range(1, len(self.noOfSprites)):
            if self.noOfSprites[i] != 0:
                flag = False
                break
        return flag
