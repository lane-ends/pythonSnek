import pygame

screen_width, screen_height = 500, 500
gridSize = 20

window = pygame.display.set_mode((screen_width, screen_height)) #gives us a sick as heck window
pygame.display.set_caption("SNEK!") #gives the window a caption

#make our character!
width = 20
height = 20
vel = 20


class Snek():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.body = []
        self.xvel = 1
        self.yvel = 0

    def move(self):
        keys = pygame.key.get_pressed()

        #grid starts at top left of the screen
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
            temp = self.x + (self.xvel * vel)
            if self.xvel < 0 and -1 < temp:
                self.x = temp
            if self.xvel > 0 and (temp + width) <= screen_width:
                self.x = temp
        if self.yvel != 0:
            temp = self.y + (self.yvel * vel)
            if self.yvel < 0 and temp > -1:
                self.y = temp 
            if self.yvel > 0 and (temp + height) <= screen_height:
                self.y = temp
    
    def draw(self, window):
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y, width, height))

#main loo!

noodle = Snek(100, 100)
run = True
while run:
    pygame.time.delay(100)
    noodle.move()
    #event : anything that happens per the user
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    

    #make our character : ) our NOODLE!!!!!!! his name is shankie (cus hell stab u)
    window.fill((0,0,0))
    noodle.draw(window)
    pygame.display.update()

#cordell is the best. i am endlessly thankful for our friendship. <3 UWU
pygame.quit()





