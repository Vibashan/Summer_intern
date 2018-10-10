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

def check_dom_region(xp,yp,xe_1,ye_1,xe_2,ye_2,xt,yt):
    s_1 = (ye_1-yp)/(xe_1-xp)
    ym_1 = (ye_1+yp)/2
    xm_1 = (xe_1+xp)/2
    s_2 = (ye_2-yp)/(xe_2-xp)
    ym_2 = (ye_2+yp)/2
    xm_2 = (xe_2+xp)/2
    if (yt-ym_1+(1/s_1)*(xt-xm_1))*(yp-ym_1+(1/s_1)*(xp-xm_1))<=0 or (yt-ym_2+(1/s_2)*(xt-xm_2))*(yp-ym_2+(1/s_2)*(xp-xm_2))<=0:
        return True

def check_dom_region_1(xp,yp,xe,ye,xt,yt):
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2
    if (yt-ym+(1/s)*(xt-xm))*(yp-ym+(1/s)*(xp-xm)) <= 0:
        return True

def restart():
    (xp,yp) = (random.randint(15,785),random.randint(15,585))
    while(1):
        (xe_1,ye_1) = (random.randint(15,785),random.randint(15,585))
        if xe_1!=xp and ye_1!=yp:
            break
    while(1):
        (xe_2,ye_2) = (random.randint(15,785),random.randint(15,585))
        if xe_2!=xp and ye_2!=yp:
            break
            
    s_1 = (ye_1-yp)/(xe_1-xp)
    ym_1 = (ye_1+yp)/2
    xm_1 = (xe_1+xp)/2
    s_2 = (ye_2-yp)/(xe_2-xp)
    ym_2 = (ye_2+yp)/2
    xm_2 = (xe_2+xp)/2
    while(1):
        (xt,yt) = (random.randint(15,785),random.randint(15,585))        
        if (yt-ym_1+(1/s_1)*(xt-xm_1))*(yp-ym_1+(1/s_1)*(xp-xm_1))>0 and (yt-ym_2+(1/s_2)*(xt-xm_2))*(yp-ym_2+(1/s_2)*(xp-xm_2))>0:
            break
    return xp,yp,xe_1,ye_1,xe_2,ye_2,xt,yt

def best_angle(xp,yp,xe_1,ye_1,xe_2,ye_2,xt,yt):
    D = deque()
    s_1 = (ye_1-yp)/(xe_1-xp)
    ym_1 = (ye_1+yp)/2
    xm_1 = (xe_1+xp)/2
    s_2 = (ye_2-yp)/(xe_2-xp)
    ym_2 = (ye_2+yp)/2
    xm_2 = (xe_2+xp)/2

    xi_1 = (s_1*(ym_1-yt)+(s_1*s_1)*xt+xm_1)/((s_1*s_1)+1)
    yi_1 = yt-s_1*xt+s_1*xi_1
    dist_eva1_2 = math.sqrt((xt-xi_1)*(xt-xi_1)+(yt-yi_1)*(yt-yi_1))

    xi_2 = (s_2*(ym_2-yt)+(s_2*s_2)*xt+xm_2)/((s_2*s_2)+1)
    yi_2 = yt-s_2*xt+s_2*xi_2
    dist_eva2_2 = math.sqrt((xt-xi_2)*(xt-xi_2)+(yt-yi_2)*(yt-yi_2))

    for i in range(0,360):
        wp = math.radians(i)
        we_1 = math.atan2((yi_1-ye_1),(xi_1-xe_1))
        we_2 = math.atan2((yi_2-ye_2),(xi_2-xe_2))
        vx_p = 1*math.cos(wp)
        vy_p = 1*math.sin(wp)
        vx_e1 = 1*math.cos(we_1)
        vy_e1 = 1*math.sin(we_1)
        vx_e2 = 1*math.cos(we_2)
        vy_e2 = 1*math.sin(we_2)

        xp_new,yp_new = movement(xp,yp,vx_p,vy_p)
        xe1_new,ye1_new = movement(xe_1,ye_1,vx_e1,vy_e1)
        xe2_new,ye2_new = movement(xe_2,ye_2,vx_e2,vy_e2)

        s1_new = (ye1_new-yp_new)/(xe1_new-xp_new)
        ym1_new = (ye1_new+yp_new)/2
        xm1_new = (xe1_new+xp_new)/2
        xi1_new = (s1_new*(ym1_new-yt)+(s1_new*s1_new)*xt+xm1_new)/((s1_new*s1_new)+1)
        yi1_new = yt-s1_new*xt+s1_new*xi1_new
        dist_eva1_1 = math.sqrt((xt-xi1_new)*(xt-xi1_new)+(yt-yi1_new)*(yt-yi1_new))

        s2_new = (ye2_new-yp_new)/(xe2_new-xp_new)
        ym2_new = (ye2_new+yp_new)/2
        xm2_new = (xe2_new+xp_new)/2
        xi2_new = (s2_new*(ym2_new-yt)+(s2_new*s2_new)*xt+xm2_new)/((s2_new*s2_new)+1)
        yi2_new = yt-s2_new*xt+s2_new*xi2_new
        dist_eva2_1 = math.sqrt((xt-xi2_new)*(xt-xi2_new)+(yt-yi2_new)*(yt-yi2_new))

        d_1 = (dist_eva1_1-dist_eva1_2)/(dist_eva1_1)
        d_2 = (dist_eva2_1-dist_eva2_2)/(dist_eva2_1)
        d = (d_1+d_2)

        D.append(d)
            
    D = np.array(D)
    max_ang = np.argmax(D)
    wp = math.radians(max_ang)
    we_1 = math.atan2((yi_1-ye_1),(xi_1-xe_1))
    we_2 = math.atan2((yi_2-ye_2),(xi_2-xe_2))

    vx_p = 1*math.cos(wp)
    vy_p = 1*math.sin(wp)
    vx_e1 = 1*math.cos(we_1)
    vy_e1 = 1*math.sin(we_1)
    vx_e2 = 1*math.cos(we_2)
    vy_e2 = 1*math.sin(we_2)

    xp,yp = movement(xp,yp,vx_p,vy_p)
    xe_1,ye_1 = movement(xe_1,ye_1,vx_e1,vy_e1)
    xe_2,ye_2 = movement(xe_2,ye_2,vx_e2,vy_e2)

    return xp,yp,xe_1,ye_1,xe_2,ye_2

def best_angle_1(xp,yp,xe,ye,xt,yt):
    D = deque()
    s = (ye-yp)/(xe-xp)
    ym = (ye+yp)/2
    xm = (xe+xp)/2
    xi = (s*(ym-yt)+(s*s)*xt+xm)/((s*s)+1)
    yi = yt-s*xt+s*xi
    dist2 = math.sqrt((xt-xi)*(xt-xi)+(yt-yi)*(yt-yi))
    for i in range(0,360):
        wp = i
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

        D.append((dist1*dist2))
            
    D = np.array(D)
    max_ang = np.argmax(D)
    wp = max_ang
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

(scr_w,scr_h) = (800,600)     # (   x  ,   y   )
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption("pur_eva")
clock = pygame.time.Clock()
FPS = 60
episode = 'restart'
mode = 'Evader_Wins'
finish = '0'
theta = 0
r = 0
win = 0
file = open('eva2_strt_pt.csv','a')

while(1):
    if finish == '1' and theta<360:
        theta+=2
        print('theta',theta)
        finish = '0'
        mode = 'Evader_Wins'
        r = 0
        win = 0
    if theta >= 360:
        break

    xp,yp,xe_1,ye_1,xt,yt = (400,300,401,110,550,230)
    xp_init,yp_init = xp,yp
    xe_2,ye_2 = xp+r*math.cos(math.radians(theta))+0.1,yp+r*math.sin(math.radians(theta))+0.1
    episode = 'start'
    while(1):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print( "Game exited by user")
                exit()

        xp,yp,xe_1,ye_1,xe_2,ye_2 = best_angle(xp,yp,xe_1,ye_1,xe_2,ye_2,xt,yt)
        xi_1,yi_1 = intersec_pt(xp,yp,xe_1,ye_1)
        xi_2,yi_2 = intersec_pt(xp,yp,xe_2,ye_2)

        if xi_1<10 or xi_1>790 or yi_1<10 or yi_1>590:
            winner = 2
            episode = 'over'
        if xi_2<10 or xi_2>790 or yi_2<10 or yi_2>590:
            winner = 2
            episode = 'over'
        
        if episode == 'start' and ((abs(xt-xi_1)<=3 and abs(yt-yi_1)<=3) or (abs(xt-xi_2)<=3 and abs(yt-yi_2)<=3)):
            print("Evader_Wins")
            print("!_0")
            winner = 0
            episode = 'over'
            mode = 'Evader_Wins'
        
        if (abs(xp-xe_1)<=1 and abs(yp-ye_1)<=1):
            eva1_dist_fin = math.sqrt((xt-xi_1)*(xt-xi_1)+(yt-yi_1)*(yt-yi_1))
            eva2_dist_fin = math.sqrt((xt-xi_2)*(xt-xi_2)+(yt-yi_2)*(yt-yi_2))
            if eva2_dist_fin>3:
                mode = 'Pursuer_Wins'
                episode = 'over'
            elif eva2_dist_fin<=3:
                mode = 'Evader_Wins'
                episode = 'over'

        if (abs(xp-xe_2)<=1 and abs(yp-ye_2)<=1):
            eva1_dist_fin = math.sqrt((xt-xi_1)*(xt-xi_1)+(yt-yi_1)*(yt-yi_1))
            eva2_dist_fin = math.sqrt((xt-xi_2)*(xt-xi_2)+(yt-yi_2)*(yt-yi_2))
            if eva1_dist_fin>3:
                mode = 'Pursuer_Wins'
                episode = 'over'
            elif eva1_dist_fin<=3:
                mode = 'Evader_Wins'
                episode = 'over'

        if episode == 'over' and mode == 'Pursuer_Wins':
            print("Pursuer_wins")
            winner = 1
        elif episode == 'start' and check_dom_region(xp,yp,xe_1,ye_1,xe_2,ye_2,xt,yt):
            print("Evader_Wins")
            print("1_1")
            winner = 0
            episode = 'over'
        
        if episode == 'over':
            if winner == 0:
                win = 0
                r+=5
                mid_ptx,mid_pty = xp_init+r*math.cos(math.radians(theta))+0.1,yp_init+r*math.sin(math.radians(theta))+0.1
                pur_lose = (mid_ptx,mid_pty)
                file = open('Nor_set_pts_pur_win_2.csv','a')
                datastr = "," + str(pur_lose) + "," + str(theta)+ "," + str(winner)+ "," + str(r)    
                file.write(datastr)
                file.write('\n')
            elif winner == 1:
                r+=2
                win+=1
                if win == 1:
                    r = r - 1
                    print(r)
                    finish = '1'
                mid_ptx,mid_pty = xp_init+r*math.cos(math.radians(theta))+0.1,yp_init+r*math.sin(math.radians(theta))+0.1 
                pur_lose = (mid_ptx,mid_pty)
                file = open('Nor_set_pts_pur_win_2.csv','a')
                datastr = "," + str(pur_lose) + "," + str(theta)+ "," + str(winner)+ "," + str(r)        
                file.write(datastr)
                file.write('\n')
            elif winner == 2:
                win = 0
                r+=5
                mid_ptx,mid_pty = xp_init+r*math.cos(math.radians(theta))+0.1,yp_init+r*math.sin(math.radians(theta))+0.1
                pur_lose = (mid_ptx,mid_pty)
                file = open('Nor_set_pts_pur_win_2.csv','a')
                datastr = "," + str(pur_lose) + "," + str(theta)+ "," + str(winner)+ "," + str(r)   
                file.write(datastr)
                file.write('\n')
            break
                   
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255,0,0), (int(xp), int(yp)),4)        #Red
        pygame.draw.circle(screen, (0,255,0), (int(xe_1), int(ye_1)),4)    #Blue
        pygame.draw.circle(screen, (0,255,255), (int(xe_2), int(ye_2)),4)  #Light_blue
        pygame.draw.circle(screen, (0,0,255), (int(xt), int(yt)),4)        #Green
        pygame.draw.circle(screen, (255,255,255), (int(xi_1), int(yi_1)),2)
        pygame.draw.circle(screen, (255,255,255), (int(xi_2), int(yi_2)),2)
        pygame.display.flip()
        clock.tick(FPS)