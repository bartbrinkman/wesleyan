#! python 3

import math
import pygame
from copy import deepcopy
import random
from pprint import pprint

pygame.init()

gridWidth = 10
gridHeight = 18
blockSize = 16
gridHorizontalOffset = 158
gridVerticalOffset = 8


patterns = {
	'30': pygame.image.load('images/pattern-3.png'),
	 '1': pygame.image.load('images/pattern-1.png'),
	 '2': pygame.image.load('images/pattern-2.png'),
	 '3': pygame.image.load('images/pattern-3.png'),
	 '4': pygame.image.load('images/pattern-4.png'),
 	 '6': pygame.image.load('images/pattern-6.png'),
	 '7': pygame.image.load('images/pattern-7.png'),
	 '8': pygame.image.load('images/pattern-8.png')
}

menu = { 
	1: pygame.image.load('images/menu-1.png'), 
	2: pygame.image.load('images/menu-2.png') 
}

sounds = {
	'drop': {
		1:  pygame.mixer.Sound('sounds/1000-Ooo.wav'),
		2:  pygame.mixer.Sound('sounds/1001-Nice Fit.wav'),
		3:  pygame.mixer.Sound('sounds/1002-Yeah.wav'),
		4:  pygame.mixer.Sound('sounds/1003-Oh my god.wav'),
		5:  pygame.mixer.Sound('sounds/1004-burp.wav'),
		6:  pygame.mixer.Sound('sounds/1005-doubleburp.wav'),
		7:  pygame.mixer.Sound('sounds/1006-gasp.wav'),
		8:  pygame.mixer.Sound('sounds/1007-Drums.wav'),
		9:  pygame.mixer.Sound('sounds/1008-Click.wav'),
		10: pygame.mixer.Sound('sounds/1009-whoa.wav'),
		11: pygame.mixer.Sound('sounds/1010-wooh.wav'),
		12: pygame.mixer.Sound('sounds/1011-step.wav'),
		13: pygame.mixer.Sound('sounds/1012-clicks.wav'),

		14: pygame.mixer.Sound('sounds/2000-Lame.wav'),
		15: pygame.mixer.Sound('sounds/2001-Lessons.wav'),
		16: pygame.mixer.Sound('sounds/2002-You-suck.wav'),
		17: pygame.mixer.Sound('sounds/2003-I hope your.wav'),
		18: pygame.mixer.Sound('sounds/2004-Son of a.wav'),
		19: pygame.mixer.Sound('sounds/2005-Good One.wav'),
		20: pygame.mixer.Sound('sounds/2006-Shattered.wav'),
		21: pygame.mixer.Sound('sounds/2007-Bozo.wav'),
		22: pygame.mixer.Sound('sounds/2008-fart.wav'),
		23: pygame.mixer.Sound('sounds/2009-otherfart.wav'),
		24: pygame.mixer.Sound('sounds/2010-You meant.wav'),
		25: pygame.mixer.Sound('sounds/2011-I assume.wav'),
		26: pygame.mixer.Sound('sounds/2012-oops.wav'),
		27: pygame.mixer.Sound('sounds/2013-whoops.wav'),
		28: pygame.mixer.Sound('sounds/2014-what for.wav'),
		29: pygame.mixer.Sound('sounds/2015-why.wav')
	},
	'destroy': {
		1: pygame.mixer.Sound('sounds/3000-Congrats.wav'),
		2: pygame.mixer.Sound('sounds/3001-I bet you.wav'),
		3: pygame.mixer.Sound('sounds/3002-longburp.wav'),
		4: pygame.mixer.Sound('sounds/3003-Addicted.wav'),
		5: pygame.mixer.Sound('sounds/3004-Cow.wav'),
		6: pygame.mixer.Sound('sounds/3005-Rooster.wav'),
		7: pygame.mixer.Sound('sounds/3006-Long Fart.wav'),
		7: pygame.mixer.Sound('sounds/3007-shots.wav')
	},
	'misc': {
		1: pygame.mixer.Sound('sounds/4004-I\'ll be back.wav'),
		2: pygame.mixer.Sound('sounds/4001-NaNaNa.wav')
	}
}

class Canvas(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.image = pygame.image.load('images/canvas.png')
		self.level = 1
		self.score = 0
		self.rowsPending = 10
		self.rowsDone = 0
		self.levelLabel = Text('Level:', [11, 100])
		self.scoreLabel = Text('Score:', [11, 116])
		self.leftLabel = Text('Rows left:', [11, 128])
		self.doneLabel = Text('Rows done:', [11, 142])
		self.levelText = Text(str(0), [100, 100])
		self.scoreText = Text(str(0), [100, 114])
		self.leftText = Text(str(0), [100, 128])
		self.doneText = Text(str(0), [100, 142])
		self.grid = Grid()
		self.nasty = 0


	def update(self, frametime):
		self.rect = self.image.get_rect()
		self.rect.x = 0
		self.rect.y = 0
		self.levelText.setContent(str(self.level))
		self.scoreText.setContent(str(self.score))
		self.leftText.setContent(str(self.rowsPending))
		self.doneText.setContent(str(self.rowsDone))
		self.nasty += 1
		if self.nasty > 100:
			while self.nasty > 0:
				y = random.randint(0, gridHeight - 1)
				x = random.randint(0, gridWidth  - 1)
				candidate = self.grid.matrix[y][x]
				if isinstance(candidate, int) == False:
					# candidate = candidate.split(':')[0]
					self.grid.matrix[y][x] = '30'
					self.nasty = 0
				
			
			sounds['misc'][2].play()
			pprint(candidate)


	def scoreBlockDown(self):
		self.score += 1

	def scoreRowCleared(self):
		self.score += 10
		self.rowsPending -= 1
		self.rowsDone += 1
		if self.rowsPending <= 0:
			self.newLevel()

	def newLevel(self):
		self.level += 1
		self.rowsPending = 10 + self.level
		self.nasty = 0
		self.grid.initialize(self.level)


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
		self.image = self.font.render(self.content, False, (0,0,0))
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

	def setContent(self, content):
		self.content = content

	def setPosition(self, position):
		self.x = position[0]
		self.y = position[1]


class Tetris():
	def shading(self, type, x, y):
		index = type.split(':')[0]
		pattern = patterns[index]
		by, bx = y, x

		if int(index) >= 30:
			self.image.blit(pattern, (bx * blockSize, by * blockSize))
			self.image.blit(pattern, (bx * blockSize + 8, by * blockSize))
			self.image.blit(pattern, (bx * blockSize, by * blockSize + 8))
			self.image.blit(pattern, (bx * blockSize + 8, by * blockSize + 8))
			return

		self.image.blit(pattern, (bx * blockSize + 4, by * blockSize + 4))
		
		if self.__class__.__name__ == 'Block':
			type = 1
			matrix = deepcopy(self.matrix)

			for i, row in enumerate(matrix):
				row = list(row)
				row.insert(0, 0)
				row.append(0)
				rl = len(row)
				matrix[i] = row
			row = [0 for i in range(rl)]
			matrix.insert(0, row)
			matrix.append(row)
			y += 1
			x += 1
		else:
			matrix = self.matrix

		# apply patterns

		if matrix[y][x - 1] == type:
			self.image.blit(pattern, (bx * blockSize - 4, by * blockSize + 4))
		if matrix[y - 1][x] == type:
			self.image.blit(pattern, (bx * blockSize + 4, by * blockSize - 4))
		if matrix[y - 1][x] == type and matrix[y][x - 1] == type and matrix[y - 1][x - 1] != type:
			self.image.blit(pattern, (bx * blockSize + 4, by * blockSize + 4))
			self.image.blit(pattern, (bx * blockSize - 4, by * blockSize + 4))
		if matrix[y - 1][x] == type and matrix[y][x - 1] == type and matrix[y - 1][x - 1] == type:
			self.image.blit(pattern, (bx * blockSize - 4, by * blockSize - 4))
			self.image.blit(pattern, (bx * blockSize - 4, by * blockSize + 4))

		# apply shading

		try:
			if matrix[y - 1][x - 1] != type and matrix[y][x - 1] != type and matrix[y - 1][x] != type: # left top
				if matrix[y + 1][x] == type: # block below is same
					if matrix[y + 1][x - 1] == type: # beyond
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + 1, by * blockSize + blockSize + 0))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + 2, by * blockSize + blockSize + 1))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + 3, by * blockSize + blockSize + 2))
					else: # straight down
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + 1, by * blockSize + blockSize))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + 2, by * blockSize + blockSize))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + 3, by * blockSize + blockSize))
				else: # partial
					pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + 1, by * blockSize + blockSize - 2))
					pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + 2, by * blockSize + blockSize - 3))
					pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + 3, by * blockSize + blockSize - 4))
		except IndexError: # bottom of canvas: partial
			pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + 1, by * blockSize + blockSize - 2))
			pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + 2, by * blockSize + blockSize - 3))
			pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + 3, by * blockSize + blockSize - 4))

		try:
			if matrix[y - 1][x] != type:
				if matrix[y][x + 1] == type:
					if matrix[y -1][x + 1] == type:
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + blockSize + 1, by * blockSize + 1))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + blockSize + 2, by * blockSize + 2))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + blockSize + 3, by * blockSize + 3))
					else:
						if matrix[y][x - 1] == type:
							pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 1, by * blockSize + 1), (bx * blockSize + blockSize - 2, by * blockSize + 1))
							pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 1, by * blockSize + 2), (bx * blockSize + blockSize - 2, by * blockSize + 2))
							pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 1, by * blockSize + 3), (bx * blockSize + blockSize - 2, by * blockSize + 3))
						else:
							pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + blockSize + 1, by * blockSize + 1))
							pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + blockSize + 2, by * blockSize + 2))
							pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + blockSize + 3, by * blockSize + 3))
				else:
					if matrix[y][x - 1] == type:
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 1, by * blockSize + 1), (bx * blockSize + blockSize - 2, by * blockSize + 1))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 2, by * blockSize + 2), (bx * blockSize + blockSize - 3, by * blockSize + 2))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 3, by * blockSize + 3), (bx * blockSize + blockSize - 4, by * blockSize + 3))
					else:
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + blockSize - 2, by * blockSize + 1))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + blockSize - 3, by * blockSize + 2))
						pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + blockSize - 4, by * blockSize + 3))
		except IndexError:
			if matrix[y][x - 1] == type:
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 1, by * blockSize + 1), (bx * blockSize + blockSize - 2, by * blockSize + 1))
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 2, by * blockSize + 2), (bx * blockSize + blockSize - 3, by * blockSize + 2))
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize - 3, by * blockSize + 3), (bx * blockSize + blockSize - 4, by * blockSize + 3))
			else:
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + 1), (bx * blockSize + blockSize - 2, by * blockSize + 1))
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + 2), (bx * blockSize + blockSize - 3, by * blockSize + 2))
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + 3), (bx * blockSize + blockSize - 4, by * blockSize + 3))

		try:
			if matrix[y][x - 1] != type and matrix[y - 1][x] == type:
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 1, by * blockSize + blockSize - 2), (bx * blockSize + 1, by * blockSize - 1))
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 2, by * blockSize + blockSize - 3), (bx * blockSize + 2, by * blockSize - 2))
				pygame.draw.line(self.image, (255,255,255), (bx * blockSize + 3, by * blockSize + blockSize - 4), (bx * blockSize + 3, by * blockSize - 3))
		except IndexError:
			pass

class Grid(Tetris, pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.initialize()
		self.x, self.y = 0, 0
		self.image = pygame.Surface((gridWidth * blockSize, gridHeight * blockSize))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.y = self.x + gridHorizontalOffset, self.y + gridVerticalOffset
		self.next = 0.0
		Grid.update(self)

	def initialize(self, level = 1):
		self.matrix = []

		try:
			self.block.kill()
			del self.block
		except Exception:
			pass

		self.block = Block(self)

		for y in range(0, gridHeight):
			row = []
			for x in range(0, gridWidth):
				row.append(0)
			self.matrix.append(row)
		
		if level == 2:
			self.matrix[17][0] = '30'
			self.matrix[16][0] = '30'
			self.matrix[15][0] = '30'
			self.matrix[14][0] = '30'
			self.matrix[13][0] = '30'
			self.matrix[12][0] = '30'
			self.matrix[11][0] = '30'
			self.matrix[10][0] = '30' 
			self.matrix[9][0]  = '30'
			self.matrix[8][0]  = '30' 
			self.matrix[7][0]  = '30' 
			self.matrix[7][1]  = '30'
			self.matrix[17][9] = '30'
			self.matrix[16][9] = '30'
			self.matrix[15][9] = '30'
			self.matrix[14][9] = '30'
			self.matrix[13][9] = '30'
			self.matrix[12][9] = '30'
			self.matrix[11][9] = '30'
			self.matrix[10][9] = '30'
			self.matrix[9][9]  = '30'
			self.matrix[8][9]  = '30'  
			self.matrix[7][9]  = '30' 
			self.matrix[7][8]  = '30'

		if level == 100:
			self.matrix[17][0] = '2'
			self.matrix[17][1] = '3'
			self.matrix[17][2] = '3'
			self.matrix[17][4] = '3'
			self.matrix[17][5] = '3'
			self.matrix[17][6] = '4'
			self.matrix[17][7] = '3'
			self.matrix[17][8] = '3'
			self.matrix[17][9] = '3'
			self.matrix[16][0] = '2'
			self.matrix[16][1] = '3'
			self.matrix[16][2] = '3'
			self.matrix[16][3] = '2'
			self.matrix[16][4] = '3'
			self.matrix[16][6] = '4'
			self.matrix[16][7] = '3'
			self.matrix[16][8] = '3'
			self.matrix[16][9] = '3'
			self.matrix[15][0] = '2'
			self.matrix[15][1] = '3'
			self.matrix[15][2] = '3'
			self.matrix[15][3] = '2'
			self.matrix[15][4] = '3'
			self.matrix[15][5] = '2'
			self.matrix[15][7] = '2'
			self.matrix[15][8] = '2'
			self.matrix[15][9] = '2'


	def update(self, frametime = 0.0):
		self.image.fill((255,255,255))
		self.checkCompleted()
		for y in range(0, gridHeight):
			for x in range(0, gridWidth):
				if self.matrix[y][x] != 0:
					pygame.draw.rect(self.image, (0,0,0), (x * blockSize, y * blockSize, blockSize, blockSize))
		self.draw()
		self.next += frametime
		if self.next > 0.5:
			self.block.moveDown()
			self.next = 0.0

	def draw(self):
		for y in range(0, gridHeight):
			for x in range(0, gridWidth):
				if (self.matrix[y][x] != 0):
					type = self.matrix[y][x]
					self.shading(type, x, y)

	def crystalize(self):
		for y, row in enumerate(self.block.matrix):
			for x, col in enumerate(row):
				if col > 0:
					self.matrix[self.block.row + y][self.block.col + x] = str(self.block.type) + ':' + str(self.block.id)
		self.block.kill()
		del self.block
		self.block = Block(self)
		pygame.mixer.stop()
		sounds['drop'][random.choice(list(sounds['drop']))].play()
		pygame.event.post(pygame.event.Event(TETRIS_BLOCK_DOWN))
		
	def checkCompleted(self):
		for y in range(0, gridHeight):
			count = 0
			for x in range(0, gridWidth):
				if self.matrix[y][x] != 0:
					count += 1
					if count >= gridWidth:
						self.destroyRow(y)

	def destroyRow(self, targetRow):
		pygame.mixer.stop()
		sounds['destroy'][random.choice(list(sounds['destroy']))].play()
		for x in range(0, gridWidth):
		 	self.matrix[targetRow][x] = 0

		for y in range(targetRow, 0, -1):
			for x in range(0, gridWidth):
				if y == 0:
					self.matrix[y][x] = 0
				else:
					self.matrix[y][x] = self.matrix[y - 1][x]

		pygame.event.post(pygame.event.Event(TETRIS_ROW_CLEARED))


class Block(Tetris, pygame.sprite.Sprite):
	id = 1
	collection = {}
	blocks = {
		1: [[1], [1], [1], [1]],
		2: [[1,0], [1,1], [0,1]],
		3: [[1,1], [1,1]],
		4: [[0,1], [1,1], [1,0]],
		# 5: [[1,0,0], [1,1,1]],
		6: [[0,0,1], [1,1,1]],
		7: [[0,1,0], [1,1,1]],
		8: [[1]],
		#9: [[1,0], [0,1], [0,1], [1,0]],
		#10: [[1,0,1], [0,0,0], [1,0,1]]
	}

	def __init__(self, grid):
		self.id = Block.id
		Block.id += 1
		Block.collection[self.id] = self
		pygame.sprite.Sprite.__init__(self, self.groups)
		self.row = 0
		self.col = 5
		self.type = random.choice(list(Block.blocks.keys()))
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

		for y, row in enumerate(self.matrix):
			for x, col in enumerate(row):
				if col == 1:
					self.shading(str(self.type), x, y)

		self.x, self.y = self.col * blockSize, self.row * blockSize
		self.rect.x, self.rect.y = self.x + gridHorizontalOffset, self.y + gridVerticalOffset

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
			if self.col + width > gridWidth:
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
			if self.col + width > gridWidth:
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
		if self.row + height > gridHeight:
			return True

		for ri, row in enumerate(self.matrix):
			for ci, col in enumerate(row):
				if col == 1 and self.grid.matrix[self.grid.block.row + ri][self.grid.block.col + ci] != 0:
					return True

		return False


pygame.init()
display = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption('Wesleyan Tetris');
screenInfo = pygame.display.Info()
screenWidth, screenHeight = int(screenInfo.current_w / 2), int(screenInfo.current_h / 2)
screen = pygame.Surface((326,304))
background = pygame.Surface((screenWidth, screenHeight))
screenPattern = pygame.image.load('images/background.png')
for x in range(int(screenWidth / 2)):
	for y in range(int(screenHeight / 2)):
		background.blit(screenPattern, (x * 2, y * 2))

pygame.mixer.Sound('sounds/4006-Shall we.wav').play()

TETRIS_BLOCK_DOWN = pygame.USEREVENT + 1
TETRIS_ROW_CLEARED = pygame.USEREVENT + 2

clock = pygame.time.Clock()
fps = 60
playtime = 0.0 # seconds

keys = [False, False, False, False, False, False] # up, down, left, right, space, p

gridGroup = pygame.sprite.Group()
blockGroup = pygame.sprite.Group()
textGroup = pygame.sprite.Group()
canvasGroup = pygame.sprite.Group()
everythingGroup = pygame.sprite.LayeredUpdates()

Grid._layer = 8
Block._layer = 9
Text._layer = 10
Canvas._layer = 1

Grid.groups = gridGroup, everythingGroup
Block.groups = blockGroup, everythingGroup
Text.groups = textGroup, everythingGroup
Canvas.groups = canvasGroup, everythingGroup

canvas = Canvas()
# grid = Grid()

gameloop = True
statePause = False
stateOver = False
stateNext = False

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
			if event.key == pygame.K_p:
				keys[5] = True
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
			if event.key == pygame.K_p:
				keys[5] = False
		if event.type == TETRIS_BLOCK_DOWN:
			canvas.scoreBlockDown()
		if event.type == TETRIS_ROW_CLEARED:
			canvas.scoreRowCleared()
	
	if statePause == False and stateOver == False and stateNext == False:	
		if keys[0]: # up
			canvas.grid.block.rotate()
			keys[0] = False

		if keys[1]: # down
			canvas.grid.block.drop()
			keys[1] = False

		if keys[2]: # left
			canvas.grid.block.moveLeft()
			keys[2] = False

		if keys[3]: # right
			canvas.grid.block.moveRight()
			keys[3] = False

		if keys[4]: # space
			canvas.grid.block.drop()
			keys[4] = False

	if keys[5] and stateOver == False and stateNext == False: # p
		keys[5] = False
		if statePause:
			statePause = False
		else:
			statePause = True
			pygame.mixer.stop()
			sounds['misc'][1].play()

	if statePause == False and stateOver == False and stateNext == False:
		everythingGroup.update(frametime)
	everythingGroup.draw(screen)
	pygame.transform.scale(background, (screenInfo.current_w, screenInfo.current_h), display)

	result = pygame.transform.scale(screen, (326* 2, 304 * 2))
	display.blit(result, (screenWidth - (((gridWidth * blockSize + gridHorizontalOffset) * 2) / 2), screenHeight - ((gridHeight * blockSize * 2) / 2)))
	
	pygame.draw.rect(display, (255,255,255), (0,0,screenWidth * 2,38))
	pygame.draw.rect(display, (0,0,0), (0,38,screenWidth * 2,2))
	display.blit(pygame.transform.scale(menu[1], (304,40)), (0,0))
	display.blit(pygame.transform.scale(menu[2], (10, 40)), (screenWidth * 2 - 10,0))
	
	pygame.display.flip()
	
pygame.quit()
exit(0)