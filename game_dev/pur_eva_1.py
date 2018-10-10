#!/usr/bin/env python

import pygame
import time
import math

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
        pygame.draw.circle(screen, (r,b,g), (int(self.x), int(self.y)),10)

def pur_eva(xp,yp,xe,ye,xt,yt):
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2

    xi = (s*(ym-yt)+(s*s)*xt+xm)/((s*s)+1)
    yi = yt-s*xt+s*xi

    wp = math.atan2((yi-yp),(xi-xp))
    we = math.atan2((yi-ye),(xi-xe))
    vx_p = 1*math.cos(wp)
    vy_p = 1*math.sin(wp)
    vx_e = 1*math.cos(we)
    vy_e = 1*math.sin(we)
    return vx_p,vy_p,vx_e,vy_e

(SCR_WID,SCR_HEI) = (640,480)   #(   x   ,    y   )
screen = pygame.display.set_mode((SCR_WID, SCR_HEI))
pygame.display.set_caption("Pong")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

(xp,yp) = (80,300)
(xe,ye) = (580,400)
(xt,yt) = (50,50) 

vx_p,vy_p,vx_e,vy_e = pur_eva(xp,yp,xe,ye,xt,yt)

pursue = Ball(xp,yp,vx_p,vy_p)
evader = Ball(xe,ye,vx_e,vy_e)
target = Ball(xt,yt,0,0)

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

    if abs(pursue.x-evader.x)<15 and abs(pursue.y-evader.y)<15:
        break

    pygame.display.flip()
    clock.tick(FPS)
