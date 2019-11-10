import pygame
import random

class Movement():

    def getDirection():
        pass

class PygameMovement(Movement):

    def getDirection(self):
        keys = pygame.key.get_pressed()
        temp = 0
        if keys[pygame.K_LEFT]:
            return "LEFT"
        if keys[pygame.K_RIGHT]:
            return "RIGHT"
        if keys[pygame.K_UP]:
            return "UP"
        if keys[pygame.K_DOWN]:
            return "DOWN"

class TextMovement(Movement):

    def __init__(self):
        self.buffer = []
        self.fillBuffer()

    def fillBuffer(self):
        with open('./input.txt', 'r') as file:
            for line in file:
                for ch in line:
                    self.buffer.append(ch)

    def getDirection(self):
        with open('./input.txt', 'r') as file:
            input = file.readLine();

class Cube():

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def move(self, newX, newY):
        self.x = newX
        self.y = newY
    
    def draw(self, window):
        global gridSize
        pygame.draw.rect(window, self.color, (self.x, self.y, gridSize, gridSize))


class Snek():

    def __init__(self, x, y, color, startingSize=2, movement=PygameMovement()):
        self.color = color
        self.head = Cube(x, y, self.color)
        self.body = []
        self.xvel = 1
        self.yvel = 0
        self.movement = movement
        for i in (range(startingSize - 1)):
            self.grow(x-(20*i), y)

    def move(self):
        global apple, gridSize
        oldHeadX, oldHeadY = self.head.x, self.head.y
        oldTailX, oldTailY = 0, 0
        if len(self.body) > 0:
            oldTailX, oldTailY = self.body[0].x, self.body[0].y
        
        keys = pygame.key.get_pressed()

        #grid starts at top left of the screen
        collide = False
        temp = 0
        direction = self.movement.getDirection()
        if direction == "LEFT":
            self.xvel = -1
            self.yvel = 0
        if direction == "RIGHT":
            self.xvel = 1
            self.yvel = 0
        if direction == "UP":
            self.xvel = 0
            self.yvel = -1
        if direction == "DOWN":
            self.xvel = 0
            self.yvel = 1
        # if keys[pygame.K_LEFT]:
        #     self.xvel = -1
        #     self.yvel = 0
        # if keys[pygame.K_RIGHT]:
        #     self.xvel = 1
        #     self.yvel = 0
        # if keys[pygame.K_UP]:
        #     self.xvel = 0
        #     self.yvel = -1
        # if keys[pygame.K_DOWN]:
        #     self.xvel = 0
        #     self.yvel = 1

        if self.xvel != 0:
            temp = self.head.x + (self.xvel * gridSize)
            collide = self.willCollide(temp, self.head.y)
        if self.yvel != 0:
            temp = self.head.y + (self.yvel * gridSize)
            collide = self.willCollide(self.head.x, temp)
        
        if not collide:
            for i, cube in enumerate(self.body):
                if i == len(self.body) - 1:
                    cube.x = self.head.x
                    cube.y = self.head.y
                else:
                    cube.x = self.body[i+1].x
                    cube.y = self.body[i+1].y
            if self.xvel != 0:
                self.head.x = temp
            if self.yvel != 0:
                self.head.y = temp

            if self.head.x == apple.x and self.head.y == apple.y:
                if len(self.body) > 0:
                    self.grow(oldTailX, oldTailY)
                else:
                    self.grow(oldHeadX, oldHeadY)
                spawnRandomApple()
            
        return collide
    
    def grow(self, x, y):
        self.body.insert(0, Cube(x, y, self.color))

    def willCollide(self, newX, newY):
        global screen_size
        valid = (0 <= newX < screen_size) and (0 <= newY < screen_size)
        collide = not valid
        if not collide:
            for cube in self.body:
                if cube.x == newX and cube.y == newY:
                    collide = True
                    break
        return collide
    
    def draw(self, window):
        self.head.draw(window)

        for cube in self.body:
            cube.draw(window)

def spawnRandomApple():
    global apple, noodle, screen_size, gridSize
    color = (255,0,0)
    rows = screen_size // gridSize
    x, y = 0, 0

    valid = False
    while not valid:
        x = random.randrange(rows) * gridSize
        y = random.randrange(rows) * gridSize

        valid = not noodle.willCollide(x, y)
        valid = noodle.head.x != x and noodle.head.y != y

    apple = Cube(x, y, color)

#main loo!
def drawGrid(window):
    global screen_size, gridSize
    color = (150,150,150)
    x, y = 0, 0
    rows = screen_size // gridSize

    for i in range(rows):
        x += gridSize
        y += gridSize

        pygame.draw.line(window, color, (x,0), (x, screen_size))
        pygame.draw.line(window, color, (0,y), (screen_size, y))

def drawGame(window):
    global noodle, apple
    window.fill((0,0,0))
    noodle.draw(window)
    apple.draw(window)
    drawGrid(window)
    pygame.display.update()


def main():
    global noodle, gridSize, screen_size

    screen_size = 1000
    gridSize = 25

    pygame.display.set_caption("SNEK!") #gives the window a caption

    window = pygame.display.set_mode((screen_size, screen_size)) #gives us a sick as heck window
    noodle = Snek(100, 100, (0, 255, 0), 1)
    spawnRandomApple()

    clock = pygame.time.Clock()
    run = True
    while run:
        pygame.time.delay(50)
        clock.tick(10)
        run = not noodle.move()
        #event : anything that happens per the user
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        #make our character : ) our NOODLE!!!!!!! his name is shankie (cus hell stab u)
        drawGame(window)

    #cordell is the best. i am endlessly thankful for our friendship. <3 UWU
    pygame.quit()

main()