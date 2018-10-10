#!/usr/bin/env python

import pygame
import time
import math
import random
import cv2
import numpy as np
import sys
import mss
from collections import deque

(scr_w,scr_h) = (600,600)     # (   x  ,   y   )
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption("pur_eva")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

class pur_eva():
    def __init__(self):
        self.vel_pur = 1
        self.vel_eva = 1
        (self.xp,self.yp) = (random.randint(15,585),random.randint(15,585))
        while(1):
            (self.xe,self.ye) = (random.randint(15,585),random.randint(15,585))
            if self.xe != self.xp and self.ye != self.yp:
                break

        self.s = (self.ye-self.yp)/(self.xe-self.xp)
        self.ym = (self.ye+self.yp)/2
        self.xm = (self.xe+self.xp)/2

        while(1):
            (self.xt,self.yt) = (random.randint(15,585),random.randint(15,585))  
            pos_tar = (self.yt-self.ym+(1/self.s)*(self.xt-self.xm))  
            pos_pur = (self.yp-self.ym+(1/self.s)*(self.xp-self.xm))
            if pos_tar*pos_pur > 0:
                break

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255,0,0), (int(self.xp), int(self.yp)),10)
        pygame.draw.circle(screen, (0,255,0), (int(self.xe), int(self.ye)),10)
        pygame.draw.circle(screen, (0,0,255), (int(self.xt), int(self.yt)),10)
        print(self.xp,self.yp,self.xe,self.ye,self.xt,self.yt)

    def game_state(self):
        pygame.event.pump()
        D = deque()
        trail = 0
        terminal = False
        self.xi = (self.s*(self.ym-self.yt)+(self.s*self.s)*self.xt+self.xm)/((self.s*self.s)+1)
        self.yi = self.yt-self.s*self.xt+self.s*self.xi
        self.dist2 = math.sqrt((self.yt-self.yi)*(self.yt-self.yi)+(self.xt-self.xi)*(self.xt-self.xi))
        print(self.xp,self.yp,self.xe,self.ye,self.xt,self.yt)

        for i in range(0,360):        
            self.wp = i
            self.we = math.atan2((self.yi-self.ye),(self.xi-self.xe))

            self.vx_p = self.vel_pur*math.cos(self.wp)
            self.vy_p = self.vel_pur*math.sin(self.wp)
            self.vx_e = self.vel_eva*math.cos(self.we)
            self.vy_e = self.vel_eva*math.sin(self.we)

            self.xp += self.vx_p
            self.yp += self.vy_p
            self.xe += self.vx_e
            self.ye += self.vy_e

            self.s = (self.ye-self.yp)/(self.xe-self.xp)
            self.ym = (self.ye+self.yp)/2
            self.xm = (self.xe+self.xp)/2
            self.xi = (self.s*(self.ym-self.yt)+(self.s*self.s)*self.xt+self.xm)/((self.s*self.s)+1)
            self.yi = self.yt-self.s*self.xt+self.s*self.xi
            self.dist1 = math.sqrt((self.yt-self.yi)*(self.yt-self.yi)+(self.xt-self.xi)*(self.xt-self.xi))

            D.append(self.dist1-self.dist2)
            if i == 359:
                D = np.array(D)
                max_ang = np.argmax(D)
                self.wp = max_ang
                self.we = math.atan2((self.yi-self.ye),(self.xi-self.xe))
                print(self.wp,self.we)

                self.vx_p = self.vel_pur*math.cos(self.wp)
                self.vy_p = self.vel_pur*math.sin(self.wp)
                self.vx_e = self.vel_eva*math.cos(self.we)
                self.vy_e = self.vel_eva*math.sin(self.we)
                print(self.vx_p,self.vy_p,self.vx_e,self.vy_e)

                self.xp = self.xp+self.vx_p
                self.yp = self.yp+self.vy_p
                self.xe = self.xe+self.vx_e
                self.ye = self.ye+self.vy_e

                self.s = (self.ye-self.yp)/(self.xe-self.xp)
                self.ym = (self.ye+self.yp)/2
                self.xm = (self.xe+self.xp)/2
                self.xi = (self.s*(self.ym-self.yt)+(self.s*self.s)*self.xt+self.xm)/((self.s*self.s)+1)
                self.yi = self.yt-self.s*self.xt+self.s*self.xi

                screen.fill((0, 0, 0))
                pygame.draw.circle(screen, (255,0,0), (int(self.xp), int(self.yp)),10)
                pygame.draw.circle(screen, (0,255,0), (int(self.xe), int(self.ye)),10)
                pygame.draw.circle(screen, (0,0,255), (int(self.xt), int(self.yt)),10)
                pygame.draw.circle(screen, (255,255,255), (int(self.xi), int(self.yi)),4)
                
                print(self.xp,self.yp,self.xe,self.ye,self.xt,self.yt)

                if abs(self.xp-self.xe)<=10 and abs(self.yp-self.ye)<=10:
                    self.__init__()

                print(self.xp,self.yp,self.xe,self.ye,self.xt,self.yt)
                pygame.display.flip()
                clock.tick(FPS)



            