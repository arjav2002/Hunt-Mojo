import pygame
import time
import random
from Sprites import*
from Level import*

grid_size = 64
display_width_grids = 16
display_height_grids = 10

red = (255, 0, 0)

b_paper_width = grid_size
b_paper_height = grid_size

heroImg = 'Images/Hero.png'
doorImg = 'Images/Door.png'
floorImg = 'Images/Floor1.png'
wallImg = 'Images/Wall1.png'
waterImg = 'Images/Water.png'
enemyImgs = ('', 'Images/BuffPaper.png', 'Images/Mario.png', 'Images/WindowsXP.png')

right_door = (15, 5)
left_door = (0, 5)
top_door = (8, 0)
bottom_door = (8, 9)

FPS = 10

class HuntForYourMojo():

	def __init__(self):
		self.game_display = pygame.display.set_mode((display_width_grids*grid_size, display_height_grids*grid_size))
		self.clock = pygame.time.Clock()
		pygame.init()
		pygame.display.set_caption('Hunt for the Lost Mojo')
		self.hp = -1
		self.main()

	def render(self):
		self.render_sprites()
		self.render_HUD()

	def render_sprites(self):
		for sprite in self.wallSpriteGroup:
			if isinstance(sprite, Wall) and sprite.id == WallIds.door.value and self.currentRoom.areDoorsUnlocked() and self.currentLevel.isDoorOperational(self.currentRoom.no, sprite):
				self.wallSpriteGroup.remove(sprite)
				self.wallSpriteGroup.add(Wall(sprite.x, sprite.y, self.currentRoom.no, floorImg, WallIds.floor.value))
			self.game_display.blit(sprite.image, (sprite.x, sprite.y))
		for sprite in self.creatureSpriteGroup:
			self.game_display.blit(sprite.image, (sprite.x, sprite.y))

	def render_HUD(self):
		self.draw_text(30, "Current Room No: {}".format(self.currentRoom.no+1), 14*grid_size, 1*grid_size)
		self.draw_text(30, "Current Level No: {}".format(self.currentLevel.lvl), 14*grid_size, 2*grid_size)
		self.draw_text(30, "Player HP: {}".format(self.p1.hp), 14*grid_size, 3*grid_size)
		if(self.currentRoom.areDoorsUnlocked()):
			self.draw_text(30, "Doors unlocked!", 14*grid_size, 4*grid_size)

	def update_sprites(self):
		for sprite in self.creatureSpriteGroup:
			if isinstance(sprite, Creature):
				sprite.update(self)

	def text_object(self, text, font):
		textSurface = font.render(text, False, (255,255,255))
		return textSurface, textSurface.get_rect()

	def draw_text(self,size,text,x,y):
		largeText = pygame.font.SysFont("Lucida Sans Roman", size)
		textSurf, textRect = self.text_object(text, largeText)
		textRect.center = (x,y)
		self.game_display.blit(textSurf, textRect)

	def draw_button(self,size,text,x1,y1,x2,y2,action = None):
		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if x1 + x2 > mouse[0] > x1 and y1 + y2 > mouse[1] > y1:
			pygame.draw.rect(self.game_display, (255,0,255), (x1, y1, x2, y2))
			self.draw_text(size,text,x1+x2/2,y1+y2/2)
			if click[0] == 1 and action != None:
				action()
		else:
			pygame.draw.rect(self.game_display, (100,100,255), (x1, y1, x2, y2))
			self.draw_text(size,text,x1+x2/2,y1+y2/2)
	
	def init_level(self, lvl):
		# randomly generate rooms layout and type and assign no
		# then initialize each 1st room
		self.currentLevel = Level(lvl)
		self.currentLevel.generate()
		self.transitionToRoom(0, top_door)

	def transitionToRoom(self,roomNo,p1Coords):
		self.currentRoom = self.currentLevel.rooms[roomNo]
		self.wallSpriteGroup = pygame.sprite.Group()
		self.creatureSpriteGroup = pygame.sprite.Group()
		for x in range(display_width_grids):
			for y in range(display_height_grids):
				id = self.currentRoom.wallGrid[y][x]
				if id == WallIds.wall.value:
					self.wallSpriteGroup.add(Wall(x*grid_size, y*grid_size, roomNo, wallImg, id))
				elif id == WallIds.floor.value:
					self.wallSpriteGroup.add(Wall(x*grid_size, y*grid_size, roomNo, floorImg, id))
				elif id == WallIds.door.value:
					self.wallSpriteGroup.add(Wall(x*grid_size, y*grid_size, roomNo, doorImg, id))
				elif id == WallIds.water.value:
					self.wallSpriteGroup.add(Wall(x*grid_size, y*grid_size, roomNo, waterImg, WallIds.water.value))
		hp_to_pass = self.hp
		if hp_to_pass < 0: hp_to_pass = 5 # hp to pass to the constructor
		self.p1 = Hero(p1Coords[0]*grid_size, p1Coords[1]*grid_size, self.currentRoom.no, heroImg, hp_to_pass, CreatureIds.hero.value)
		self.creatureSpriteGroup.add(self.p1)
		self.currentRoom.creatureGrid[int(self.p1.y/grid_size)][int(self.p1.x/grid_size)] = CreatureIds.hero.value
		for x in range(display_width_grids):
			for y in range(display_height_grids):
				id = self.currentRoom.creatureGrid[y][x]
				if id != CreatureIds.noCreature.value and id != CreatureIds.hero.value:
					self.creatureSpriteGroup.add(EnemySprite(x*grid_size, y*grid_size, roomNo, enemyImgs[id], 2, id))
	
	def finishLevel(self):
		self.init_level(self.currentLevel.lvl+1)

	def main_menu(self):
		
		menu_exit = False

		self.game_display.fill((random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))

		while not menu_exit:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

		
			self.draw_text(120,"Hunt for your Lost Mojo",500,200)
			self.draw_button(60,"Go!",200,400,100,100,self.game_loop)
			self.draw_button(60,"Exit",700,400,100,100,self.quit_game)

			pygame.display.update()
			self.clock.tick(FPS)

	def game_loop(self):
		self.init_level(1)
		game_exit = False
		while not game_exit:

			for event in pygame.event.get():
				
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()

				if event.type == pygame.KEYDOWN:
					keys_pressed = pygame.key.get_pressed()

					if event.key == pygame.K_e:
						game_exit = True

					if keys_pressed[pygame.K_LEFT]:
						if self.p1.x >= 1*grid_size:
							self.p1.move(self, 3)
						elif self.currentRoom.wallGrid[int(self.p1.y/grid_size)][int(self.p1.x/grid_size)] == WallIds.door.value and self.currentRoom.areDoorsUnlocked():
							to_trans = self.currentLevel.getLeftRoomNo(self.currentRoom.no)
							if to_trans >= 0:
								self.transitionToRoom(to_trans, right_door)

					if keys_pressed[pygame.K_RIGHT]:
						if self.p1.x <= (display_width_grids-2)*grid_size:
							self.p1.move(self, 1)
						elif self.currentRoom.wallGrid[int(self.p1.y/grid_size)][int(self.p1.x/grid_size)] == WallIds.door.value and self.currentRoom.areDoorsUnlocked():
							to_trans = self.currentLevel.getRightRoomNo(self.currentRoom.no)
							if to_trans >= 0:
								self.transitionToRoom(to_trans, left_door)

					if keys_pressed[pygame.K_UP]:
						if self.p1.y >= 1*grid_size:
							self.p1.move(self, 0)
						elif self.currentRoom.wallGrid[int(self.p1.y/grid_size)][int(self.p1.x/grid_size)] == WallIds.door.value and self.currentRoom.areDoorsUnlocked():
							to_trans = self.currentLevel.getTopRoomNo(self.currentRoom.no)
							if to_trans >= 0:
								self.transitionToRoom(to_trans, bottom_door)

					if keys_pressed[pygame.K_DOWN]:
						if self.p1.y <= (display_height_grids-2)*grid_size:
							self.p1.move(self, 2)
						elif self.currentRoom.wallGrid[int(self.p1.y/grid_size)][int(self.p1.x/grid_size)] == WallIds.door.value and self.currentRoom.areDoorsUnlocked():
							to_trans = self.currentLevel.getBottomRoomNo(self.currentRoom.no)
							if to_trans >= 0:
								self.transitionToRoom(to_trans, top_door)
					self.update_sprites()
					self.p1.check_hp(self)

			self.render()
			pygame.display.update()
			self.clock.tick(FPS)

	def game_over(self):

		gameover = False

		while not gameover:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_e:
						gameover = True

			self.draw_text(200,"GAME OVER",500,200)
			self.draw_text(100,"Press E to exit to Main Menu",500,400)
			pygame.display.update()
			self.clock.tick(FPS)

		self.init_level(1)
		self.main_menu()

	def quit_game(self):
		pygame.quit()
		quit()

	def main(self):
		self.main_menu()
		pygame.quit()
		quit()


if __name__ == '__main__':
	game = HuntForYourMojo()