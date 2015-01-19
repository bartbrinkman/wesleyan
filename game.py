#! python 3

import math
import pygame
from copy import deepcopy
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
		self.font = pygame.font.Font('fonts/Chicago.ttf', 8)
		self.x, self.y = position[0], position[1]
		self.setContent(content)

	def update(self, frametime):
		pass

	def setContent(self, content):
		self.content = content
		self.image = self.font.render(self.content, False, (0,0,0))
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
		self.checkCompleted()
		for y in range(0, canvasHeight):
			for x in range(0, canvasWidth):
				if self.matrix[y][x] != 0:
					pygame.draw.rect(self.image, (0,0,0), (x * blockSize, y * blockSize, blockSize, blockSize))

		self.draw()

		self.next += frametime
		if self.next > 0.5:
			self.block.moveDown()
			self.next = 0.0

	def draw(self):
		for y in range(0, canvasHeight):
			for x in range(0, canvasWidth):
				if (self.matrix[y][x] != 0):
					type = self.matrix[y][x]
					self.shading(type, x, y)
					
					
	def shading(self, type, x, y):
		# the amount of hard-coding here says we need to develop a generalized shading routine

		pattern = patterns[type.split(':')[0]]
		self.image.blit(pattern, (x * blockSize + 4, y * blockSize + 4))

		if self.matrix[y][x - 1] != type:
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 1, y * blockSize + 1), (x * blockSize - 2 + blockSize, y * blockSize + 1))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 1, y * blockSize + 2), (x * blockSize - 3 + blockSize, y * blockSize + 2))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 1, y * blockSize + 3), (x * blockSize - 4 + blockSize, y * blockSize + 3))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 1, y * blockSize + 1), (x * blockSize + 1, y * blockSize + blockSize - 2))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 2, y * blockSize + 2), (x * blockSize + 2, y * blockSize + blockSize - 3))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 3, y * blockSize + 3), (x * blockSize + 3, y * blockSize + blockSize - 4))

		if self.matrix[y][x - 1] == type: # same type left of block
			pygame.draw.line(self.image, (255,255,255), (x * blockSize - 1, y * blockSize + 1), (x * blockSize - 2 + blockSize, y * blockSize + 1))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize - 2, y * blockSize + 2), (x * blockSize - 3 + blockSize, y * blockSize + 2))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize - 3, y * blockSize + 3), (x * blockSize - 4 + blockSize, y * blockSize + 3))
			self.image.blit(pattern, (x * blockSize - 4, y * blockSize + 4))

		if self.matrix[y - 1][x] == type: # same type top of block
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 1, y * blockSize - 1), (x * blockSize + 1, y * blockSize + blockSize - 2))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 2, y * blockSize - 2), (x * blockSize + 2, y * blockSize + blockSize - 3))
			pygame.draw.line(self.image, (255,255,255), (x * blockSize + 3, y * blockSize - 3), (x * blockSize + 3, y * blockSize + blockSize - 4))
			self.image.blit(pattern, (x * blockSize + 4, y * blockSize - 4))

		if self.matrix[y - 1][x] == type and self.matrix[y][x - 1] == type and self.matrix[y - 1][x - 1] != type:
			self.image.blit(pattern, (x * blockSize + 4, y * blockSize + 4))
			self.image.blit(pattern, (x * blockSize - 4, y * blockSize + 4))

		if self.matrix[y - 1][x] == type and self.matrix[y][x - 1] == type and self.matrix[y - 1][x - 1] == type:
			self.image.blit(pattern, (x * blockSize - 4, y * blockSize - 4))
			self.image.blit(pattern, (x * blockSize - 4, y * blockSize + 4))

		try:
			if self.matrix[y][x - 1] == type and self.matrix[y - 1][x] == type and self.matrix[y - 1][x + 1] == type and self.matrix[y][x + 1] != type:
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 1, y * blockSize + blockSize - 4), (x * blockSize + 1, y * blockSize + blockSize - 2))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 2, y * blockSize + blockSize - 4), (x * blockSize + 2, y * blockSize + blockSize - 3))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 3, y * blockSize + blockSize - 4), (x * blockSize + 3, y * blockSize + blockSize - 4))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 2, y * blockSize + 1), (x * blockSize + blockSize - 2, y * blockSize + 1))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 3, y * blockSize + 1), (x * blockSize + blockSize - 3, y * blockSize + 2))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 4, y * blockSize + 1), (x * blockSize + blockSize - 4, y * blockSize + 3))
			if self.matrix[y - 1][x] == type and self.matrix[y + 1][x] == type and self.matrix[y - 1][x + 1] != type and self.matrix[y][x + 1] != type and self.matrix[y + 1][x + 1] != type:
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 2, y * blockSize + 1), (x * blockSize + blockSize - 2, y * blockSize + 1))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 3, y * blockSize + 1), (x * blockSize + blockSize - 3, y * blockSize + 2))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 4, y * blockSize + 1), (x * blockSize + blockSize - 4, y * blockSize + 3))
			if self.matrix[y - 1][x] == type and self.matrix[y - 1][x + 1] != type and self.matrix[y][x + 1] != type:
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 2, y * blockSize + 1), (x * blockSize + blockSize - 2, y * blockSize + 1))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 3, y * blockSize + 1), (x * blockSize + blockSize - 3, y * blockSize + 2))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 4, y * blockSize + 1), (x * blockSize + blockSize - 4, y * blockSize + 3))	
			if self.matrix[y - 1][x] == type and self.matrix[y][x + 1] == type and self.matrix[y - 1][x + 1] != type:
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 2, y * blockSize + 1), (x * blockSize + blockSize - 2, y * blockSize + 1))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 3, y * blockSize + 1), (x * blockSize + blockSize - 3, y * blockSize + 2))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 4, y * blockSize + 1), (x * blockSize + blockSize - 4, y * blockSize + 3))
		except IndexError:
			pass

		try:
			if self.matrix[y][x - 1] == type and self.matrix[y + 1][x - 1] != type and self.matrix[y + 1][x] != type:
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 1, y * blockSize + blockSize - 4), (x * blockSize + 1, y * blockSize + blockSize - 2))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 2, y * blockSize + blockSize - 4), (x * blockSize + 2, y * blockSize + blockSize - 3))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 3, y * blockSize + blockSize - 4), (x * blockSize + 3, y * blockSize + blockSize - 4))
		except IndexError:
			if self.matrix[y][x - 1] == type:
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 1, y * blockSize + blockSize - 4), (x * blockSize + 1, y * blockSize + blockSize - 2))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 2, y * blockSize + blockSize - 4), (x * blockSize + 2, y * blockSize + blockSize - 3))
				pygame.draw.line(self.image, (0,0,0), (x * blockSize + 3, y * blockSize + blockSize - 4), (x * blockSize + 3, y * blockSize + blockSize - 4))

		if x == canvasWidth - 1:
			try:
				if self.matrix[y - 1][x] == type and self.matrix[y - 1][x + 1] != type and self.matrix[y][x + 1] != type and self.matrix[y + 1][x + 1] != type:
					pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 2, y * blockSize + 1), (x * blockSize + blockSize - 2, y * blockSize + 1))
					pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 3, y * blockSize + 1), (x * blockSize + blockSize - 3, y * blockSize + 2))
					pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 4, y * blockSize + 1), (x * blockSize + blockSize - 4, y * blockSize + 3))
			except IndexError:
				if self.matrix[y - 1][x] == type:
					pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 2, y * blockSize + 1), (x * blockSize + blockSize - 2, y * blockSize + 1))
					pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 3, y * blockSize + 1), (x * blockSize + blockSize - 3, y * blockSize + 2))
					pygame.draw.line(self.image, (0,0,0), (x * blockSize + blockSize - 4, y * blockSize + 1), (x * blockSize + blockSize - 4, y * blockSize + 3))


	def crystalize(self):
		for y, row in enumerate(self.block.matrix):
			for x, col in enumerate(row):
				if col > 0:
					self.matrix[grid.block.row + y][grid.block.col + x] = str(grid.block.type) + ':' + str(grid.block.id)
		self.block.kill()
		del self.block
		self.block = Block(self)
		

	def checkCompleted(self):
		for y in range(0, canvasHeight):
			count = 0
			for x in range(0, canvasWidth):
				if self.matrix[y][x] != 0:
					count += 1
					if count >= canvasWidth:
						self.destroyRow(y)

	def destroyRow(self, targetRow):
		for x in range(0, canvasWidth):
		 	self.matrix[targetRow][x] = 0
		
		for y in range(targetRow, 0, -1):
			pprint(y)
			for x in range(0, canvasWidth):
				if y == 0:
					self.matrix[y][x] = 0
				else:
					self.matrix[y][x] = self.matrix[y - 1][x]


class Block(pygame.sprite.Sprite):
	id = 1
	collection = {}
	blocks = {
		
		#1: [[1], [1], [1], [1]],
		#2: [[1,0], [1,1], [0,1]],
		#3: [[1,1], [1,1]],
		#4: [[0,1], [1,1], [1,0]],
		
		# 5: [[1,0,0], [1,1,1]],
		
		6: [[0,0,1], [1,1,1]],
		7: [[0,1,0], [1,1,1]],
		#8: [[1]]
	}

	def __init__(self, grid):
		self.id = Block.id
		Block.id += 1
		Block.collection[self.id] = self
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.row = 0
		self.col = 5
		self.type = choice(list(Block.blocks.keys()))
		self.matrix = Block.blocks[self.type]
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

		for y, row in enumerate(self.matrix):
			for x, col in enumerate(row):
				if col == 1:
					pygame.draw.rect(self.image, (0,0,0), (x * blockSize, y * blockSize, blockSize, blockSize))

		self.x, self.y = self.col * blockSize, self.row * blockSize
		self.rect.x, self.rect.y = self.x, self.y

	def moveLeft(self):
		self.col -= 1
		if self.col < 0:
			self.col += 1
			return

		for ri, row in enumerate(self.matrix):
			for ci, col in enumerate(row):
				if col == 1 and self.grid.matrix[self.row + ri][self.col + ci] != 0:
					self.col += 1
					return

		Block.update(self)

	def moveRight(self):
		self.col += 1
		for row in self.matrix:
			width = len(row)
			if self.col + width > canvasWidth:
				self.col -= 1
				return

		for ri, row in enumerate(self.matrix):
			for ci, col in enumerate(row):
				if col == 1 and self.grid.matrix[self.row + ri][self.col + ci] != 0:
					self.col -= 1
					return

		Block.update(self)

	def rotate(self):
		new = list(zip(*self.matrix[::-1]))
		for row in new:
			width = len(row)
			if self.col + width > canvasWidth:
				return

		for ri, row in enumerate(new):
			for ci, col in enumerate(row):
				if col == 1 and self.grid.matrix[self.row + ri][self.col + ci] != 0:
					return
			
		self.matrix = new
		Block.update(self)

	def drop(self):
		while(self.isDown() == False):
			self.row += 1
		self.row -= 1
		self.grid.crystalize()

	def moveDown(self):
		self.row += 1
		if self.isDown():
			self.row -= 1
			self.grid.crystalize()

	def isDown(self):
		height = len(self.matrix)
		if self.row + height > canvasHeight:
			return True

		for ri, row in enumerate(self.matrix):
			for ci, col in enumerate(row):
				if col == 1 and self.grid.matrix[grid.block.row + ri][grid.block.col + ci] != 0:
					return True

		return False


pygame.init()
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Wesleyan Tetris');
screenInfo = pygame.display.Info()
screenWidth, screenHeight = int(screenInfo.current_w / 2), int(screenInfo.current_h / 2)
screen = pygame.Surface((screenWidth, screenHeight))
screenPattern = pygame.image.load('images/background.png')
for x in range(int(screenWidth / 2)):
	for y in range(int(screenHeight / 2)):
		screen.blit(screenPattern, (x * 2, y * 2))

sound_4006 = pygame.mixer.Sound('sounds/4006-Shall we.wav')
sound_4006.play()

patterns = {
	'1': pygame.image.load('images/pattern-1.png'),
	'2': pygame.image.load('images/pattern-2.png'),
	'3': pygame.image.load('images/pattern-3.png'),
	'4': pygame.image.load('images/pattern-4.png'),
	'6': pygame.image.load('images/pattern-6.png'),
	'7': pygame.image.load('images/pattern-7.png'),
	'8': pygame.image.load('images/pattern-8.png')
}

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
Text('This is Tetris', [2,0])

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
		grid.block.drop()
		keys[1] = False

	if keys[2]: # left
		grid.block.moveLeft()
		keys[2] = False

	if keys[3]: # right
		grid.block.moveRight()
		keys[3] = False

	if keys[4]: # space
		grid.block.drop()
		keys[4] = False

	everythingGroup.update(frametime)
	everythingGroup.draw(screen)
	pygame.transform.scale(screen, (screenInfo.current_w, screenInfo.current_h), display)
	pygame.display.flip()
	
pygame.quit()
exit(0)