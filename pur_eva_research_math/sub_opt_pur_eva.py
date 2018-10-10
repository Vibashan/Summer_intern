#!/usr/bin/env python

import pygame
import time
import math
import random
import cv2
import numpy as np
import mss
from collections import deque

def movement(x,y,speed_x,speed_y):
    x += speed_x
    y += speed_y
    return x,y

def restart():
    (xp,yp) = (random.randint(15,585),random.randint(15,585))
    while(1):
        (xe,ye) = (random.randint(15,585),random.randint(15,585))
        if (xe,ye) != (xp,yp):
            break
            
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2
    while(1):
        (xt,yt) = (random.randint(15,585),random.randint(15,585))        
        if (yt-ym+(1/s)*(xt-xm))*(yp-ym+(1/s)*(xp-xm)) > 0:
            break
    return xp,yp,xe,ye,xt,yt

def best_angle(xp,yp,xe,ye,xt,yt,i1):
    D = deque()
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2
    xi = (s*(ym-yt)+(s*s)*xt+xm)/((s*s)+1)
    yi = yt-s*xt+s*xi
    dist2 = math.sqrt((xt-xi)*(xt-xi)+(yt-yi)*(yt-yi))
    for i in range(0,360):
        wp = math.radians(i)
        we = math.atan2((yi-ye),(xi-xe))
        vx_p = 1*math.cos(wp)
        vy_p = 1*math.sin(wp)
        vx_e = 1*math.cos(we)
        vy_e = 1*math.sin(we)

        xp_new,yp_new = movement(xp,yp,vx_p,vy_p)
        xe_new,ye_new = movement(xe,ye,vx_e,vy_e)

        s_new = (ye_new-yp_new)/(xe_new-xp_new)
        ym_new = (ye_new+yp_new)/2
        xm_new = (xe_new+xp_new)/2
        xi_new = (s_new*(ym_new-yt)+(s_new*s_new)*xt+xm_new)/((s_new*s_new)+1)
        yi_new = yt-s_new*xt+s_new*xi_new
        dist1 = math.sqrt((xt-xi_new)*(xt-xi_new)+(yt-yi_new)*(yt-yi_new))

        D.append((dist1-dist2))
            
    D = np.array(D)
    max_ang = np.argmax(D)
    wp = math.radians(i1)
    we = math.atan2((yi-ye),(xi-xe))

    vx_p = 1*math.cos(wp)
    vy_p = 1*math.sin(wp)
    vx_e = 1*math.cos(we)
    vy_e = 1*math.sin(we)

    xp,yp = movement(xp,yp,vx_p,vy_p)
    xe,ye = movement(xe,ye,vx_e,vy_e)

    return xp,yp,xe,ye

def intersec_pt(xp,yp,xe,ye):
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2
    xi = (s*(ym-yt)+(s*s)*xt+xm)/((s*s)+1)
    yi = yt-s*xt+s*xi
    return xi,yi

(scr_w,scr_h) = (600,600)     # (   x  ,   y   )
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption("pur_eva")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60
i1=0

while(1):
    xp,yp,xe,ye,xt,yt = 40,500,41,50,350,530
    screen.fill((0, 0, 0))
    i1+=10
    print(i1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print( "Game exited by user")
                exit()

        xp,yp,xe,ye = best_angle(xp,yp,xe,ye,xt,yt,i1)
        xi,yi = intersec_pt(xp,yp,xe,ye)

        if abs(xp-xe)<=4 and abs(yp-ye)<=4:
            break
        if xi>590 or xi<10 or yi>590 or yi<10:
            break
        if abs(xi-xt)<=2 and abs(yi-yt)<=2:
            time.sleep(2)
            break

        #screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255,0,0), (int(xp), int(yp)),3)
        pygame.draw.circle(screen, (0,255,0), (int(xe), int(ye)),3)
        pygame.draw.circle(screen, (0,0,255), (int(xt), int(yt)),3)
        pygame.draw.circle(screen, (255,255,255), (int(xi), int(yi)),1)
        pygame.display.flip()
        clock.tick(FPS)
        time.sleep(0.02)
