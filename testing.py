import pygame
import random

screen_width, screen_height = 500, 500
gridSize = 20

window = pygame.display.set_mode((screen_width, screen_height)) #gives us a sick as heck window
pygame.display.set_caption("SNEK!") #gives the window a caption

#grid sizes!
width = 20
height = width

#snek move snapping!
vel = width

class Cube():

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    
    def move(self, newX, newY):
        self.x = newX
        self.y = newY
    
    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, width, height))


class Snek():

    def __init__(self, x, y, color, startingSize=2):
        self.color = color
        self.head = Cube(x, y, self.color)
        self.body = []
        self.xvel = 1
        self.yvel = 0
        for i in (range(startingSize - 1)):
            self.grow(x-(20*i), y)

    def move(self):
        global apple
        moved = False
        oldx, oldy = self.head.x, self.head.y
        oldTailX, oldTailY = 0, 0
        if len(self.body) > 0:
            oldTailX, oldTailY = self.body[0].x, self.body[0].y
        keys = pygame.key.get_pressed()

        #grid starts at top left of the screen
        collide = False
        temp = 0
        if keys[pygame.K_LEFT]:
            self.xvel = -1
            self.yvel = 0
        if keys[pygame.K_RIGHT]:
            self.xvel = 1
            self.yvel = 0
        if keys[pygame.K_UP]:
            self.xvel = 0
            self.yvel = -1
        if keys[pygame.K_DOWN]:
            self.xvel = 0
            self.yvel = 1

        if self.xvel != 0:
            temp = self.head.x + (self.xvel * vel)
            collide = self.willCollide(temp, self.head.y)
            if self.xvel < 0 and -1 < temp and (not collide):
                moved = True
            if self.xvel > 0 and (temp + width) <= screen_width and (not collide):
                moved = True
        if self.yvel != 0:
            temp = self.head.y + (self.yvel * vel)
            collide = self.willCollide(self.head.x, temp)
            if self.yvel < 0 and temp > -1 and (not collide):
                moved = True
            if self.yvel > 0 and (temp + height) <= screen_height and (not collide):
                moved = True
        
        if moved:
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
                self.grow(oldTailX, oldTailY)
                spawnRandomApple()
            
        return collide
    
    def grow(self, x, y):
        self.body.insert(0, Cube(x, y, self.color))

    def willCollide(self, newX, newY):
        collide = False
        collide = (0 <= newX <= screen_width) and (0 <= newY <= screen_height)
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
    global noodle
    color = (255,0,0)
    rows = screen_width // width
    x, y = 0, 0

    valid = False
    while not valid:
        x = random.randrange(rows) * width
        y = random.randrange(rows) * width

        valid = not noodle.willCollide(x, y)
        valid = noodle.head.x != x and noodle.head.y != y

    global apple
    apple = Cube(x, y, color)

#main loo!
def drawGrid(window):
    color = (150,150,150)
    x, y = 0, 0
    rows = screen_width // width

    for i in range(rows):
        x += width
        y += width

        pygame.draw.line(window, color, (x,0), (x, screen_width))
        pygame.draw.line(window, color, (0,y), (screen_width, y))

def drawGame(window):
    global noodle, apple
    window.fill((0,0,0))
    noodle.draw(window)
    apple.draw(window)
    drawGrid(window)
    pygame.display.update()

def main():
    global noodle
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