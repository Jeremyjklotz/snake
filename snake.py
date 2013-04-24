
import pygame, math, random
pygame.init()
pygame.display.init()
pygame.font.init()

#define four directions
UP = 0
RIGHT = 90
DOWN = 180
LEFT = 270
dirs = [UP, RIGHT, DOWN, LEFT]

#define the size of a basic grid
GRID_SIZE = 10

#define the size of window
WIDTH = 800
HEIGHT = 600

#let the snake stop
STOP = 1000000

class Food(pygame.sprite.Sprite):
	'''	class of food
		x,y stand for its location
		generate method reset the location
	'''
	def __init__(self,screen):
		self.screen = screen
		self.generate()
		
	def generate(self):
		# while True:
		self.x = random.randint(0, WIDTH / GRID_SIZE - 1) * GRID_SIZE
		self.y = random.randint(0, HEIGHT / GRID_SIZE - 1) * GRID_SIZE
		self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
		
	def update(self):
		pygame.draw.rect(self.screen, (0, 0xFF, 0), self.rect, 0)
		
class Snake(pygame.sprite.Sprite):
	'''class of normal snake
	'''
	def __init__(self, screen, food, location, color, dir):
		pygame.sprite.Sprite.__init__(self)
		#self.other = otherSnake
		self.screen = screen
		self.food = food
		self.color = color
		self.dir = dir
		self.speedCtrl = 0
		self.speed = 3
		self.width = GRID_SIZE
		self.init_length = 10
		self.startPos = location
		self.Pos_X = []
		self.Pos_Y = []
		self.point = 0
		for i in range(self.init_length):
			self.Pos_X.append(self.startPos[0] + i * self.width)
			self.Pos_Y.append(self.startPos[1])
		
	def checkFoodCollision(self):
		#detect the collision with food
		if self.Pos_X[len(self.Pos_X) - 1] == self.food.x \
			and self.Pos_Y[len(self.Pos_X) - 1] == self.food.y:
			#if true, replace the food
			self.food.generate()
			#and increase the snake's length
			dx = 0
			dy = 0
			if self.dir == UP:
				dy = GRID_SIZE
			elif self.dir == DOWN:
				dy = -GRID_SIZE
			elif self.dir == LEFT:
				dx = GRID_SIZE
			elif self.dir == RIGHT:
				dx = -GRID_SIZE
			self.Pos_X.insert(0, self.Pos_X[0] + dx)
			self.Pos_Y.insert(0, self.Pos_Y[0] + dy)
			#add up 100 points each time
			self.point += 100
			#check and speed up every 500 
			#unless it reaches the maximum speed
			if self.point != 0 and self.point % 500 == 0:
				self.speed = max(self.speed - 1, 1)
				
	def outOfScreen(self):
		print self.Pos_X[-1], self.Pos_Y[-1]
		if (self.Pos_X[-1] < 0 or self.Pos_X[-1] > WIDTH or self.Pos_Y[-1] < 0 or self.Pos_Y[-1] > HEIGHT):
			return True
		else:
			return False
			
	def update(self):
		curLen = len(self.Pos_X)
		#control the speed of the snake
		if self.speedCtrl == self.speed:
			self.speedCtrl = 0
			#calculate and update the new position of the snake
			for i in range(curLen - 1):
				self.Pos_X[i] = self.Pos_X[i+1]
				self.Pos_Y[i] = self.Pos_Y[i+1]
			if self.dir == RIGHT:
				self.Pos_X[curLen - 1] += self.width
			elif self.dir == DOWN:
				self.Pos_Y[curLen - 1] += self.width
			elif self.dir == LEFT:
				self.Pos_X[curLen - 1] -= self.width
			elif self.dir == UP:
				self.Pos_Y[curLen - 1] -= self.width
			
			self.checkFoodCollision()
		else:
			self.speedCtrl += 1
		
		#draw the snake
		for i in range(curLen):
			Rect = [self.Pos_X[i], self.Pos_Y[i], self.width, self.width]
			pygame.draw.rect(self.screen, self.color, Rect, 0)

class UserSnake(Snake):
	'''
		inherit from the Snake class
	'''
	def __init__(self, screen, food, location, color, dir):
		Snake.__init__(self, screen, food, location, color, dir)
		
	def contorlledByUser(self, pressKeys):
		if pressKeys[pygame.K_LEFT] and self.dir != RIGHT:
			self.dir = LEFT
		elif pressKeys[pygame.K_RIGHT] and self.dir != LEFT:
			self.dir = RIGHT
		elif pressKeys[pygame.K_UP] and self.dir != DOWN:
			self.dir = UP
		elif pressKeys[pygame.K_DOWN] and self.dir != UP:
			self.dir = DOWN
			
class AISnake(Snake):
	'''
		inherit from the Snake class
	'''
	def __init__(self, screen, food, location, color, dir):
		Snake.__init__(self, screen, food, location, color, dir)
	
	def turnLeft(self):
		self.dir -= 90
		self.dir += 360
		self.dir %= 360
		
	def turnRight(self):
		self.dir += 90
		self.dir %= 360 
		
	def hasObstacle(self, x, y):  
		if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
			return True
		point_color = self.screen.get_at((x, y))
		if point_color != (0xFF, 0xFF, 0xFF) and point_color != (0, 0xFF, 0):
			#print (x , y),
			return True
		
	def controlledByAI(self):
		if self.speedCtrl == self.speed:
			dx = self.Pos_X[-1] - self.food.x
			dy = self.Pos_Y[-1] - self.food.y
			#scores for four directions
			scores = [0, 0, 0, 0]
			#if have obstacles on some direction, add -200
			for dir in dirs:
				if dir == UP and self.hasObstacle(self.Pos_X[-1], self.Pos_Y[-1] - GRID_SIZE):
					scores[0] += -200
				elif dir == RIGHT and self.hasObstacle(self.Pos_X[-1] + GRID_SIZE, self.Pos_Y[-1]):
					scores[1] += -200
				elif dir == DOWN and self.hasObstacle(self.Pos_X[-1], self.Pos_Y[-1] + GRID_SIZE):
					scores[2] += -200
				elif dir == LEFT and self.hasObstacle(self.Pos_X[-1] - GRID_SIZE, self.Pos_Y[-1]):
					scores[3] += -200
			#add score on the right directions
			if dx < 0:
				scores[1] += 100
			elif dx > 0:
				scores[3] += 100
			if dy < 0:
				scores[2] += 100
			elif dy > 0:
				scores[0] += 100
			#get the best direction and turn to it 
			nextDir = scores.index(max(scores)) * 90
			#print nextDir, scores
			delta = self.dir - nextDir
			
			if delta == -90 or delta == 270:
				self.turnRight()
			elif delta == 90 or delta == -270:
				self.turnLeft()
			elif abs(delta) == 180:
				if scores[(self.dir + 90) % 360 / 90] >= scores[(self.dir - 90) % 360 / 90]:
					self.turnRight()
				else:
					self.turnLeft()

class World(pygame.sprite.Sprite):
	'''class of World, which can create Food and Snakes, including
		aiSnake and userSnake and decide which is the winner by checking
		the collision between them
	'''
	def __init__(self, screen):
		pygame.sprite.Sprite.__init__(self)
		self.screen = screen
		self.reset()
		
	def reset(self):
		self.food = Food(self.screen)
		self.userSnake = UserSnake(self.screen, self.food, [10,100], (255, 0, 0), RIGHT)
		self.aiSnake = AISnake(self.screen, self.food, [500,400], (0, 0, 255), LEFT)
		self.winner = ""
		self.hasPrinted = False
		
	def acceptUserControl(self, pressKeys):
		self.userSnake.contorlledByUser(pressKeys)
		
	def checkWinner(self):
		#check aiSnake
		for i in range(len(self.aiSnake.Pos_X)):
			if (self.aiSnake.Pos_X[i], self.aiSnake.Pos_Y[i]) == (self.userSnake.Pos_X[-1], self.userSnake.Pos_Y[-1]) or self.userSnake.outOfScreen():
				self.winner = "AI"
				self.aiSnake.speed = self.userSnake.speed = STOP
				break
			if (self.aiSnake.Pos_X[-1], self.aiSnake.Pos_Y[-1]) == (self.aiSnake.Pos_X[i], self.aiSnake.Pos_Y[i])\
				and i != len(self.aiSnake.Pos_X) - 1 or self.aiSnake.outOfScreen():
				self.winner = "user"
				self.aiSnake.speed = self.userSnake.speed = STOP
				break
				
		#check self.userSnake
		for i in range(len(self.userSnake.Pos_X)):
			if (self.aiSnake.Pos_X[-1], self.aiSnake.Pos_Y[-1]) == (self.userSnake.Pos_X[i], self.userSnake.Pos_Y[i]):
				self.winner = "user"
				self.aiSnake.speed = self.userSnake.speed = STOP
				break
			if (self.userSnake.Pos_X[-1], self.userSnake.Pos_Y[-1]) == (self.userSnake.Pos_X[i], self.userSnake.Pos_Y[i])\
				and i != len(self.userSnake.Pos_X) - 1:
				self.winner = "AI"
				self.aiSnake.speed = self.userSnake.speed = STOP
				break;
		
		if self.aiSnake.speed == STOP and not self.hasPrinted:
			text =  "Winner is " + self.winner +" ! score: user = " \
					+ str(self.userSnake.point) + " vs AI = "\
					+ str(self.aiSnake.point) + "  Press Y to try again, N to quit"
			font = pygame.font.Font(None, 30)
			self.textImg = font.render(text, 1, (0,0,0))
			self.hasPrinted = True
			
	def acceptCmd(self, key):
		if key[pygame.K_y] and self.hasPrinted:
			self.reset()
		elif key[pygame.K_n] and self.hasPrinted:
			exit()
			
	def update(self):
		if not self.hasPrinted:
			self.checkWinner()
		else:
			self.screen.blit(self.textImg, (50, HEIGHT/2))
		self.userSnake.update()
		self.aiSnake.update()
		self.food.update()

def main():
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption ("Snake")
	background = pygame.Surface(screen.get_size())
	background.fill((0xFF, 0xFF, 0xFF))
	
	world = World(screen)
	
	clock = pygame.time.Clock()
	keepGoing = True
	hasPrinted = False
	while keepGoing:
		clock.tick(30)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				keepGoing = False
			if event.type == pygame.KEYDOWN:
				world.acceptUserControl(pygame.key.get_pressed())
				world.acceptCmd(pygame.key.get_pressed())
				
		world.aiSnake.controlledByAI()
		screen.blit(background, (0, 0))
		world.update()
		pygame.display.flip()
		
if __name__ == "__main__":
	main()