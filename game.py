#! /usr/bin/python

import pygame
from pygame import *

WIN_WIDTH = 256*3
WIN_HEIGHT = 224*3
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

currLevel = 0
moveNext = False
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0

pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Use arrows to move!")

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/stand.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightstand1 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/run1.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightwalk1 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/run2.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightwalk2 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/run3.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightwalk3 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/jump.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightjump1 = character

def main():
   
	timer = pygame.time.Clock()

	up = down = left = right = running = False
	platforms = []
	#bg = Background('bg1.png', 0, 0)
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	bgImg = pygame.image.load('images/bg1.png')
	background.blit(bgImg, (0,0))
	screen.blit(background, (0,0))
	pygame.display.update()
	#bg = Surface((WIN_WIDTH,WIN_HEIGHT)).convert()
	entities = pygame.sprite.Group()
   
	x = y = 0
	level = nextLevel()

	# build the level
	for row in level:
		for col in row:
			if col == "P":
				p = Platform(x, y)
				platforms.append(p)
				entities.add(p)
			if col == "e":
				e = ExitBlock(x, y)
				platforms.append(e)
				entities.add(e)
			x += 16*3
		y += 16*3
		x = 0

	total_level_width  = len(level[0])*16*3
	total_level_height = len(level)*16*3
	camera = Camera(complex_camera, total_level_width, total_level_height)
	player = Player(60, total_level_height - 32)
	entities.add(player)

	while 1:
		timer.tick(60)
		
		for e in pygame.event.get():
			if e.type == QUIT: raise SystemExit("QUIT")
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				raise SystemExit("ESCAPE")
			if e.type == KEYDOWN and e.key == K_UP:
				up = True
			if e.type == KEYDOWN and e.key == K_DOWN:
				down = True
			if e.type == KEYDOWN and e.key == K_LEFT:
				left = True
			if e.type == KEYDOWN and e.key == K_RIGHT:
				right = True
			if e.type == KEYDOWN and e.key == K_SPACE:
				running = True

			if e.type == KEYUP and e.key == K_UP:
				up = False
			if e.type == KEYUP and e.key == K_DOWN:
				down = False
			if e.type == KEYUP and e.key == K_RIGHT:
				right = False
			if e.type == KEYUP and e.key == K_LEFT:
				left = False

		#screen.blit(bg,(0,0))
		screen.blit(background,(0,0))
		camera.update(player)
		# update player, draw everything else
		player.update(up, down, left, right, running, platforms)     
		
		#if reached portal, reset variables and draw next map
		if (moveNext == True):
			player = Player(16*3, 16*3)
			x=0
			y=0
			platforms=[]
			level = nextLevel()
			entities = pygame.sprite.Group()
		
			for row in level:
				for col in row:
					if col == "P":
						p = Platform(x, y)
						platforms.append(p)
						entities.add(p)
					if col == "e":
						e = ExitBlock(x, y)
						platforms.append(e)
						entities.add(e)
					x += 16*3
				y += 16*3
				x = 0
			entities.add(player)
			total_level_width  = len(level[0])*16*3
			total_level_height = len(level)*16*3
			camera = Camera(complex_camera, total_level_width, total_level_height)
			
		for e in entities:
			screen.blit(e.image, camera.apply(e))

		pygame.display.update()

class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		self.state = Rect(0, 0, width, height)

	def apply(self, target):
		return target.rect.move(self.state.topleft)

	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

	l = min(0, l)                           # stop scrolling at the left edge
	l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
	t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
	t = min(0, t)                           # stop scrolling at the top
	return Rect(l, t, w, h)

def nextLevel():
	x = 0
	y = 0
	level = []
	global currLevel
	if currLevel == 0:
		level = [
		"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
		"P                                          P",
		"P                                          e",
		"P                                          e",
		"P                        PPPPPPPPP      PPPP",
		"P                  PP                      P",
		"P                PP                        P",
		"P                                          P",
		"P    PPPPPPPP                              P",
		"P            PP                            P",
		"P                          PPPPPPP         P",
		"P                 PPPPPP                   P",
		"P                                          P",
		"P         PPPPPPP                          P",
		"P       PP                                 P",
		"P                     PPPPPP               P",
		"P                                          P",
		"P   PPPPPPPPPPP                            P",
		"P                                          P",
		"P                 PPPPPPPPPPP              P",
		"P                            PP            P",
		"P                              PP          P",
		"P                                          P",
		"P                                          P",
		"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
	elif currLevel == 1:
		level = [
				"PPPPPPPPPPPPPPPPPPPPPPPP",
				"                       P",
				"                       P",
				"PPP                    P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",           
				"P                      P",
				"PPPPPPPPPPPPPPPPPPPPPPPP"]
	elif currLevel == 1:
		level = [
				"PPPPPPPPPPPPPPPPPPPPPPPP",
				"                       P",
				"                       P",
				"PPP                    P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",
				"P                      P",           
				"P                      P",
				"PPPPPPPPPPPPPPPPPPPPPPPP"]
				  
	global moveNext
	moveNext = False
	currLevel+=1
	
	return level
	
class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

class Player(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.xvel = 0
		self.yvel = 0
		self.faceright = True
		self.onGround = False
		self.airborne = True
		self.counter = 0
		self.image = knightstand1
		self.rect = Rect(x, y, 16*4, 32*3)

	def update(self, up, down, left, right, running, platforms):
		if up:
			# only jump if on the ground
			if self.onGround: self.yvel -= 10
		if down:
			pass
		if running:
			self.xvel = 12
		if left:
			self.xvel = -8
			self.faceright = False
		if right:
			self.xvel = 8
			self.faceright = True
		if not self.onGround:
			# only accelerate with gravity if in the air
			self.yvel += 0.35
			# max falling speed
			if self.yvel > 100: self.yvel = 100
		if not(left or right):
			self.xvel = 0
		if self.yvel < 0 or self.yvel > 1.2: self.airborne = True
		# increment in x direction
		self.rect.left += self.xvel
		# do x-axis collisions
		self.collide(self.xvel, 0, platforms)
		# increment in y direction
		self.rect.top += self.yvel
		# assuming we're in the air
		self.onGround = False;
		# do y-axis collisions
		self.collide(0, self.yvel, platforms)

		self.animate()

	def collide(self, xvel, yvel, platforms):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if isinstance(p, ExitBlock):
					#go to next level based on currLevel variable
					global moveNext
					moveNext = True
					#pygame.event.post(pygame.event.Event(QUIT))
				if xvel > 0:
					self.rect.right = p.rect.left
					print("collide right")
				if xvel < 0:
					self.rect.left = p.rect.right
					print("collide left")
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.airborne = False
					self.yvel = 0
				if yvel < 0:
					self.rect.top = p.rect.bottom
	def animate(self):

		if self.xvel > 0 or self.xvel < 0:
			self.walkloop()
			if self.airborne: self.updatecharacter(knightjump1)
		else:
			self.updatecharacter(knightstand1)
			if self.airborne: self.updatecharacter(knightjump1)

	def walkloop(self):
		if self.counter == 5:
			self.updatecharacter(knightwalk1)
		elif self.counter == 10:
			self.updatecharacter(knightwalk2)
		elif self.counter == 15:
			self.updatecharacter(knightwalk3)
			self.counter = 0
		self.counter = self.counter + 1

	def updatecharacter(self, ansurf):
		if not self.faceright: ansurf = pygame.transform.flip(ansurf,True,False)
		self.image = ansurf

class Platform(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/block.png").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3))
		self.rect = Rect(x, y, 16*3, 16*3)

	def update(self):
		pass
		
class Background(Entity):
	def __init__(self, image, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load(image).convert()
		
		
class ExitBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(Color("#0033FF"))

if __name__ == "__main__":
	main()