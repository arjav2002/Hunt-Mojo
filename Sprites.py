import pygame
import enum
import random

display_width_grids = 16
display_height_grids = 10

class WallIds(enum.Enum):
	wall = 0
	floor = 1
	door = 2
	water = 3

class CreatureIds(enum.Enum):
	hero = 0
	bPaper = 1
	mario = 2
	xp = 3
	noCreature = -1

grid_size = 64

class Sprite(pygame.sprite.Sprite):

	def __init__(self, x, y, room_no, path, id = 0):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect()
		self.width = grid_size
		self.height = grid_size
		self.room_no = room_no
		self.x = x
		self.y = y
		self.id = id
		
class Creature(Sprite):
	def __init__(self, x, y, room_no, path, hp, id = 0):
		Sprite.__init__(self, x, y, room_no, path, id)
		self.hp = hp
		if self.id == CreatureIds.xp.value:
			pygame.mixer.music.load("Sound/XPBassBoosted.ogg")
			pygame.mixer.music.set_volume(0.3)
			pygame.mixer.music.play()

	# wall grid
	def move(self, mojo, dir):
		wallGrid = mojo.currentRoom.wallGrid
		creatureGrid = mojo.currentRoom.creatureGrid
		xIn = int(self.x/grid_size)
		yIn = int(self.y/grid_size)
		if dir == 0:
			self.move_up(mojo, xIn, yIn, wallGrid, creatureGrid)
		elif dir == 1:
			self.move_right(mojo, xIn, yIn, wallGrid, creatureGrid)
		elif dir == 2:
			self.move_down(mojo, xIn, yIn, wallGrid, creatureGrid)
		else:
			self.move_left(mojo, xIn, yIn, wallGrid, creatureGrid)
		if self.id == CreatureIds.hero.value and wallGrid[int(self.y/grid_size)][int(self.x/grid_size)] == WallIds.water.value:
			self.die(mojo)

	def move_up(self, mojo, xIn, yIn, wallGrid, creatureGrid):
		if yIn <= 0: return
		if(wallGrid[yIn-1][xIn] != WallIds.wall.value and creatureGrid[yIn-1][xIn] == CreatureIds.noCreature.value):
			if wallGrid[yIn-1][xIn] == WallIds.water.value:
				if self.id == CreatureIds.hero.value:
					self.die(mojo)
				else: return
			creatureGrid[yIn-1][xIn] = self.id
			creatureGrid[yIn][xIn] = CreatureIds.noCreature.value
			self.y -= grid_size
	
	def move_down(self, mojo, xIn, yIn, wallGrid, creatureGrid):
		if yIn >= display_height_grids-1 : return
		if(wallGrid[yIn+1][xIn] != WallIds.wall.value and creatureGrid[yIn+1][xIn] == CreatureIds.noCreature.value):
			if wallGrid[yIn+1][xIn] == WallIds.water.value:
				if self.id == CreatureIds.hero.value:
					self.die(mojo)
				else: return
			creatureGrid[yIn+1][xIn] = self.id
			creatureGrid[yIn][xIn] = CreatureIds.noCreature.value
			self.y += grid_size
	
	def move_left(self, mojo, xIn, yIn, wallGrid, creatureGrid):
		if xIn <= 0 : return 
		if(wallGrid[yIn][xIn-1] != WallIds.wall.value and creatureGrid[yIn][xIn-1] == CreatureIds.noCreature.value):
			if wallGrid[yIn][xIn-1] == WallIds.water.value:
				if self.id == CreatureIds.hero.value:
					self.die(mojo)
				else: return
			creatureGrid[yIn][xIn-1] = self.id
			creatureGrid[yIn][xIn] = CreatureIds.noCreature.value
			self.x -= grid_size
	
	def move_right(self, mojo, xIn, yIn, wallGrid, creatureGrid):
		if xIn >= display_width_grids-1 : return
		if(wallGrid[yIn][xIn+1] != WallIds.wall.value and creatureGrid[yIn][xIn+1] == CreatureIds.noCreature.value):
			if wallGrid[yIn][xIn+1] == WallIds.water.value:
				if self.id == CreatureIds.hero.value:
					self.die(mojo)
				else: return
			creatureGrid[yIn][xIn+1] = self.id
			creatureGrid[yIn][xIn] = CreatureIds.noCreature.value
			self.x += grid_size

	def die(self, mojo):
		mojo.currentRoom.noOfSprites[self.id] -= 1
		mojo.creatureSpriteGroup.remove(self)
		mojo.currentRoom.creatureGrid[int(self.y/grid_size)][int(self.x/grid_size)] = CreatureIds.noCreature.value
		if self.id == CreatureIds.hero.value:
			mojo.game_over()
		elif self.id == CreatureIds.xp.value:
			pygame.mixer.music.load("Sound/Windows XP Shutdown Earrape.ogg")
			pygame.mixer.music.set_volume(0.3)
			pygame.mixer.music.play()
		else:
			mojo.p1.hp += 3

	def update(self, mojo):
		pass
		
class Wall(Sprite):
	def __init__(self, x, y, room_no, path, id = 0):
		Sprite.__init__(self, x, y, room_no, path, id)	

class Hero(Creature):

	def __init__(self, x, y, room_no, path, hp, id = 0):
		Creature.__init__(self, x, y, room_no, path, hp, id)

	def check_hp(self, mojo):
		mojo.hp = self.hp
		if self.hp == 0:
			self.die(mojo)

class EnemySprite(Creature):

	def __init__(self, x, y, room_no, path, hp, id = 0):
		Creature.__init__(self, x, y, room_no, path, hp, id)

	def update(self, mojo):
		creatureGrid = mojo.currentRoom.creatureGrid
		xIn = int(self.x/grid_size)
		yIn = int(self.y/grid_size)
		moveConsidered = -1

		if self.id == CreatureIds.bPaper.value:
			if(self.x < mojo.p1.x):
				moveConsidered = 1 #right
			elif(self.x > mojo.p1.x):
				moveConsidered = 3 #left
			elif(self.y > mojo.p1.y):
				moveConsidered = 0 #up
			elif(self.y < mojo.p1.y):
				moveConsidered = 2 #down
			self.move(mojo ,moveConsidered)

			# if there is a clash
			if (moveConsidered == 1	and xIn < display_width_grids-1 and creatureGrid[yIn][xIn+1] == CreatureIds.hero.value) or (moveConsidered == 2 and yIn < display_height_grids-1  and creatureGrid[yIn+1][xIn] == CreatureIds.hero.value) or (moveConsidered == 3 and xIn > 0 and creatureGrid[yIn][xIn-1] == CreatureIds.hero.value) or (moveConsidered == 0 and yIn > 0 and creatureGrid[yIn-1][xIn] == CreatureIds.hero.value):	
				# then do this
				self.hp -= 1
				mojo.p1.hp -= 1

				if self.hp == 0:
					self.die(mojo)

		if self.id == CreatureIds.mario.value:
			if(self.y < mojo.p1.y):
				moveConsidered = 2
			elif(self.y > mojo.p1.y):
				moveConsidered = 0
			elif(self.x > mojo.p1.x):
				moveConsidered = 3
			elif(self.x < mojo.p1.x):
				moveConsidered = 1
			self.move(mojo ,moveConsidered)

			# if there is a clash
			if (moveConsidered == 1	and xIn < display_width_grids-1 and creatureGrid[yIn][xIn+1] == CreatureIds.hero.value) or (moveConsidered == 2 and yIn < display_height_grids-1 and creatureGrid[yIn+1][xIn] == CreatureIds.hero.value) or (moveConsidered == 3 and xIn > 0 and creatureGrid[yIn][xIn-1] == CreatureIds.hero.value) or (moveConsidered == 0 and yIn > 0 and creatureGrid[yIn-1][xIn] == CreatureIds.hero.value):	
				# then do this
				self.hp -= 1
				mojo.p1.hp -= 1

				if self.hp == 0:
					self.die(mojo)

		if self.id == CreatureIds.xp.value:
			moveConsidered = random.randrange(0,4)
			self.move(mojo ,moveConsidered)

			# if there is a clash
			if (moveConsidered == 1	and xIn < display_width_grids-1 and creatureGrid[yIn][xIn+1] == CreatureIds.hero.value) or (moveConsidered == 2 and yIn < display_height_grids-1 and creatureGrid[yIn+1][xIn] == CreatureIds.hero.value) or (moveConsidered == 3 and xIn > 0 and creatureGrid[yIn][xIn-1] == CreatureIds.hero.value) or (moveConsidered == 0 and yIn > 0 and creatureGrid[yIn-1][xIn] == CreatureIds.hero.value):	
				#then do this
				self.hp -= 1
				mojo.p1.hp -= 1

				if self.hp == 0:
					self.die(mojo)

		if(mojo.currentRoom.no == len(mojo.currentLevel.rooms)-1) and mojo.currentRoom.areDoorsUnlocked():
			mojo.finishLevel()