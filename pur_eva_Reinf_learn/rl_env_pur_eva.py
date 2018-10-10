#!/usr/bin/env python

import pygame
import time
import math
import random
import cv2
import numpy as np
import sys
import mss

(scr_w,scr_h) = (300,300)     # (   x  ,   y   )
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption("pur_eva")
pygame.font.init()
clock = pygame.time.Clock()
FPS = 60

class pur_eva():
    def __init__(self):
        self.vel_pur = 1.5
        self.vel_eva = 1.5
        (self.xp,self.yp) = (random.randint(15,285),random.randint(15,285))
        while(1):
            (self.xe,self.ye) = (random.randint(15,285),random.randint(15,285))
            if self.xe != self.xp and self.ye != self.yp:
                break
            
        self.s = (self.ye-self.yp)/(self.xe-self.xp)
        self.ym = (self.ye+self.yp)/2
        self.xm = (self.xe+self.xp)/2
        while(1):
            (self.xt,self.yt) = (random.randint(15,285),random.randint(15,285))        
            if (self.yt-self.ym+(1/self.s)*(self.xt-self.xm))*(self.yp-self.ym+(1/self.s)*(self.xp-self.xm)) > 0:
                break
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255,0,0), (int(self.xp), int(self.yp)),14)
        pygame.draw.circle(screen, (0,255,0), (int(self.xe), int(self.ye)),11)
        pygame.draw.circle(screen, (0,0,255), (int(self.xt), int(self.yt)),8)

    def game_state(self, input_action):
        pygame.event.pump()
        terminal = False

        self.xi = (self.s*(self.ym-self.yt)+(self.s*self.s)*self.xt+self.xm)/((self.s*self.s)+1)
        self.yi = self.yt-self.s*self.xt+self.s*self.xi
        self.dist2 = math.sqrt((self.yt-self.yi)*(self.yt-self.yi)+(self.xt-self.xi)*(self.xt-self.xi))
        
        self.wp = math.radians(input_action)
        self.we = math.atan2((self.yi-self.ye),(self.xi-self.xe))

        self.vx_p = self.vel_pur*math.cos(self.wp)
        self.vy_p = self.vel_pur*math.sin(self.wp)
        self.vx_e = self.vel_eva*math.cos(self.we)
        self.vy_e = self.vel_eva*math.sin(self.we)

        self.xp += self.vx_p
        self.yp += self.vy_p
        self.xe += self.vx_e
        self.ye += self.vy_e
        if self.xp > 285 or self.xp < 15 or self.yp < 15 or self.yp > 285:
            reward = -1
            terminal = True
            image_data = pygame.surfarray.array3d(pygame.display.get_surface())
            self.__init__()
            return image_data, reward, terminal

        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255,0,0), (int(self.xp), int(self.yp)),14)
        pygame.draw.circle(screen, (0,255,0), (int(self.xe), int(self.ye)),11)
        pygame.draw.circle(screen, (0,0,255), (int(self.xt), int(self.yt)),8)
        pygame.draw.circle(screen, (255,255,255), (int(self.xi), int(self.yi)),3)

        self.s = (self.ye-self.yp)/(self.xe-self.xp)
        self.ym = (self.ye+self.yp)/2
        self.xm = (self.xe+self.xp)/2
        self.xi = (self.s*(self.ym-self.yt)+(self.s*self.s)*self.xt+self.xm)/((self.s*self.s)+1)
        self.yi = self.yt-self.s*self.xt+self.s*self.xi
        self.dist1 = math.sqrt((self.yt-self.yi)*(self.yt-self.yi)+(self.xt-self.xi)*(self.xt-self.xi))

        if (self.yt-self.ym+(1/self.s)*(self.xt-self.xm))*(self.yp-self.ym+(1/self.s)*(self.xp-self.xm)) > 0:
            if self.dist1-self.dist2 >= -0.2:
                reward = 0.8
            else:
                reward = -0.4

        if abs(self.xp-self.xe)<=13 and abs(self.yp-self.ye)<=13:
            reward = 1
            terminal = True
            self.__init__()

        elif (self.yt-self.ym+(1/self.s)*(self.xt-self.xm))*(self.yp-self.ym+(1/self.s)*(self.xp-self.xm)) < 0:
            reward = -1
            terminal = True
            self.__init__()

        pygame.display.flip()
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        clock.tick(FPS)

        return image_data, reward, terminal