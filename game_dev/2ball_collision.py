import pygame
import time

class Ball():
    def __init__(self,pos_x,pos_y,vel_x,vel_y):
        self.x, self.y = pos_x, pos_y
        self.speed_x = vel_x
        self.speed_y = vel_y
        self.size = 15
    
    def movement(self):
        self.x += self.speed_x
        self.y += self.speed_y

        #wall col
        if self.y <= 0:
            self.speed_y *= -1
        elif self.y >= SCR_HEI-self.size:
            self.speed_y *= -1

        if self.x <= 0:
            self.speed_x *= -1
        elif self.x >= SCR_WID-self.size:
            self.speed_x *= -1

    def draw(self,r,g,b):
        pygame.draw.circle(screen, (r,b,g), (self.x, self.y),10)


SCR_WID, SCR_HEI = 640, 480 #(y,x)
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Pong")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

pursue = Ball(600,400,1,1)
evader = Ball(30,40,1,1)
target = Ball(100,100,0,0)

while True:
    #process
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print( "Game exited by user")
                exit()
    ##process
    #logic
    pursue.movement()
    evader.movement()
    target.movement()
    ##logic
    #draw
    screen.fill((0, 0, 0))
    pursue.draw(250,0,0)
    evader.draw(0,0,250)
    target.draw(0,250,0)

    pygame.display.flip()
    clock.tick(FPS)
