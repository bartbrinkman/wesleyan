#! python 3

import math
import pygame
from random import choice
from pprint import pprint

canvasWidth = 10
canvasHeight = 18
blockSize = 16


class Text(pygame.sprite.Sprite):
	id = 1
	collection = {}
	def __init__(self, content, position):
		self.id = Text.id
		Text.id += 1
		Text.collection[self.id] = self
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.font = pygame.font.Font(False, 9)
		self.x, self.y = position[0], position[1]
		self.setContent(content)

	def update(self, frametime):
		pass

	def setContent(self, content):
		self.content = content
		self.image = self.font.render(self.content, False, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def setPosition(self, position):
		self.x = position[0]
		self.y = position[1]
		self.rect.x = self.x
		self.rect.y = self.y


class Grid(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.matrix = []
		for y in range(0, canvasHeight):
			row = []
			for x in range(0, canvasWidth):
				row.append(0)
			self.matrix.append(row)
		self.x, self.y = 0, 0
		self.image = pygame.Surface((canvasWidth * blockSize, canvasHeight * blockSize))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.x, self.y
		self.block = Block(self)
		self.next = 0.0
		Grid.update(self)

	def update(self, frametime = 0.0):
		self.image.fill((255,255,255))
		self.next += frametime
		if self.next > 0.5:
			self.block.moveDown()
			self.next = 0.0

	def crystalize(self):
		for ri, row in enumerate(self.block.matrix):
			for ci, col in enumerate(row):
				if col == 1:
					self.matrix[grid.block.row + ri][grid.block.col + ci] = 1

		pprint(self.matrix)


class Block(pygame.sprite.Sprite):
	blocks = [
		[[1], [1], [1], [1]],			
		[[1,0], [1,1], [0,1]],
		[[1,1], [1,1]],
		[[0,1], [1,1], [1,0]],
		[[1,0,0], [1,1,1]],
		[[0,0,1], [1,1,1]]
	]
	def __init__(self, grid):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.sprite = pygame.image.load('block.png')
		self.row = 0
		self.col = 5
		self.matrix = choice(Block.blocks)
		self.grid = grid
		Block.update(self)

	def update(self, frametime = 0.0):
		x, y = 0, 0
		for row in self.matrix:
			x = 0
			for col in row:
				x += 1
			y += 1

		self.image = pygame.Surface((x * blockSize, y * blockSize)).convert_alpha()
		self.image.fill((255,255,255,0))
		self.rect = self.image.get_rect()

		x, y = 0, 0
		for row in self.matrix:
			x = 0
			for col in row:
				if col == 1:
					self.image.blit(self.sprite, (x * blockSize, y * blockSize))
				x += 1
			y += 1			

		self.x, self.y = self.col * blockSize, self.row * blockSize
		self.rect.x, self.rect.y = self.x, self.y

	def moveLeft(self):
		self.col -= 1
		if self.col < 0:
			self.col = 0
		Block.update(self)

	def moveRight(self):
		self.col += 1
		for row in self.matrix:
			width = len(row)
		if self.col + width > canvasWidth:
			self.col -= 1	
		Block.update(self)

	def rotate(self):
		# self.matrix = list(zip(*self.matrix))
		self.matrix = list(zip(*self.matrix[::-1]))
		Block.update(self)

	def moveDown(self):
		self.row += 1
		Block.evaluateDown(self)
		Block.update(self)

	def evaluateLeft(self):
		pass

	def evaluateRight(self):
		pass

	def evaluateDown(self):
		# check whether the current position goes past the canvas or if it's anywhere it shouldn't be
		# if it is, put it back one row, add it to the matrix and re-init another block on the grid

		height = len(self.matrix)
		if self.row + height > canvasHeight:
			self.row -= 1
			self.grid.crystalize()
			self.grid.block = Block(self.grid)
			return 

		for ri, row in enumerate(self.matrix):
			for ci, col in enumerate(row):
				if col == 1 and self.grid.matrix[grid.block.row + ri][grid.block.col + ci] == 1:
					self.row -= 1
					self.grid.crystalize()
					self.grid.block = Block(self.grid)
					return
	
		





pygame.init()
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Wesleyan Tetris');
screenInfo = pygame.display.Info()
screenWidth, screenHeight = int(screenInfo.current_w / 2), int(screenInfo.current_h / 2)
screen = pygame.Surface((screenWidth, screenHeight))

sound_4006 = pygame.mixer.Sound('wave/4006_shall_we.wav')
sound_4006.play()

SOME_EVENT = pygame.USEREVENT + 1

clock = pygame.time.Clock()
fps = 60
playtime = 0.0 # seconds

keys = [False, False, False, False, False] # up, down, left, right, space

gridGroup = pygame.sprite.Group()
blockGroup = pygame.sprite.Group()
textGroup = pygame.sprite.Group()
everythingGroup = pygame.sprite.LayeredUpdates()

Grid._layer = 8
Block._layer = 9
Text._layer = 10

Grid.groups = gridGroup, everythingGroup
Block.groups = blockGroup, everythingGroup
Text.groups = textGroup, everythingGroup

grid = Grid()

gameloop = True
while gameloop:
	frametime = clock.tick(fps) / 1000
	playtime += frametime
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameloop = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				keys[0] = True
			if event.key == pygame.K_DOWN:
				keys[1] = True
			if event.key == pygame.K_LEFT:
				keys[2] = True
			if event.key == pygame.K_RIGHT:
				keys[3] = True
			if event.key == pygame.K_SPACE:
				keys[4] = True
			if event.key == pygame.K_ESCAPE:
				gameloop = False
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_UP:
				keys[0] = False
			if event.key == pygame.K_DOWN:
				keys[1] = False
			if event.key == pygame.K_LEFT:
				keys[2] = False
			if event.key == pygame.K_RIGHT:
				keys[3] = False
			if event.key == pygame.K_SPACE:
				keys[4] = False
				
	if keys[0]: #up
		grid.block.rotate()
		keys[0] = False

	if keys[1]: # down
		grid.block.moveDown()

	if keys[2]: # left
		grid.block.moveLeft()
		keys[2] = False

	if keys[3]: # right
		grid.block.moveRight()
		keys[3] = False

	if keys[4]: # space
		grid.block.moveDown()

	display.fill((255,0,0))
	everythingGroup.update(frametime)
	everythingGroup.draw(screen)
	pygame.transform.scale(screen, (screenInfo.current_w, screenInfo.current_h), display)
	pygame.display.flip()
	
pygame.quit()
exit(0)