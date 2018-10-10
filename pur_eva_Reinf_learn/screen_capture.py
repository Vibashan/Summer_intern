#!/usr/bin/env python

import pygame
#!/usr/bin/env python

import time
import math
import random
import cv2
import numpy as np
import sys
import mss

class Ball():
    def __init__(self,pos_x,pos_y,vel_x,vel_y):
        self.x, self.y = pos_x, pos_y
        self.speed_x = vel_x
        self.speed_y = vel_y
        self.size = 15
    
    def movement(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self,r,g,b):
        pygame.draw.circle(screen, (r,b,g), (int(self.x), int(self.y)),11)

def pur_eva(xp,yp,xe,ye,xt,yt):
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2

    xi = (s*(ym-yt)+(s*s)*xt+xm)/((s*s)+1)
    yi = yt-s*xt+s*xi

    wp = math.atan2((yi-yp),(xi-xp))
    we = math.atan2((yi-ye),(xi-xe))
    vx_p = 1.5*math.cos(wp)
    vy_p = 1.5*math.sin(wp)
    vx_e = 1.5*math.cos(we)
    vy_e = 1.5*math.sin(we)
    return vx_p,vy_p,vx_e,vy_e

def restart():
    (xp,yp) = (random.randint(15,625),random.randint(15,465))
    while(1):
        (xe,ye) = (random.randint(15,625),random.randint(15,465))
        if (xe,ye) != (xp,yp):
            break
            
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2
    while(1):
        (xt,yt) = (random.randint(15,625),random.randint(15,465))        
        if (yt-ym+(1/s)*(xt-xm))*(yp-ym+(1/s)*(xp-xm)) > 0:
            break
    return xp,yp,xe,ye,xt,yt

def game_logic():
    pursue.movement()
    evader.movement()
    target.movement()

    screen.fill((0, 0, 0))
    pursue.draw(250,0,0)
    evader.draw(0,0,250)
    target.draw(0,250,0)

(scr_w,scr_h) = (640,480)     # (   x  ,   y   )
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption("pur_eva")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

xp,yp,xe,ye,xt,yt = restart()
vx_p,vy_p,vx_e,vy_e = pur_eva(xp,yp,xe,ye,xt,yt)
pursue = Ball(xp,yp,vx_p,vy_p)
evader = Ball(xe,ye,vx_e,vy_e)
target = Ball(xt,yt,0,0)
pursue.draw(250,0,0)
evader.draw(0,0,250)
target.draw(0,250,0) 

while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print( "Game exited by user")
                exit()
    game_logic()

    monitor = {'top': 51, 'left': 55, 'width': 640, 'height': 480}
    img_np = np.array(mss.mss().grab(monitor))
    cv2.imshow('OpenCV/Numpy normal', img_np)
    cv2.waitKey(1)

    if abs(pursue.x-evader.x)<16 and abs(pursue.y-evader.y)<16:
        time.sleep(0.5)
        xp,yp,xe,ye,xt,yt = restart()
    vx_p,vy_p,vx_e,vy_e = pur_eva(xp,yp,xe,ye,xt,yt)
    pursue = Ball(xp,yp,vx_p,vy_p)
    evader = Ball(xe,ye,vx_e,vy_e)
    target = Ball(xt,yt,0,0)
    pursue.draw(250,0,0)
    evader.draw(0,0,250)
    target.draw(0,250,0)
        
    pygame.display.flip()
    clock.tick(FPS)
