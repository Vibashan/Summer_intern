#!/usr/bin/env python
#python tkinter
#python version 3.3.2
#http://www.cnblogs.com/hongten/p/hongten_python_pong.html

from tkinter import *

''' 
    Judge
    two balls
    {
     Center: A(x1, y1) Radius: r X-axis Speed: Vax Y-axis Velocity: Vay
     Center: B(x2,y2) Radius: RX Axis Velocity: Vbx Y Axis Velocity: Vby
    }
    Collision conditions are:
    1. The centerline distance of two small balls is not greater than the sum of the two ball radiuses. (r+R), namely:
    {
       (x2 - x1)^2 + (y2 - y1)^2 <= (r + R)^2
    }
    2. After the ball collides, the number of two balls is exchanged, ie:
    {
        tempVax = Vax
        tempVay = Vay
        Vax = Vbx
        Vay = Vby
        Vbx = tempVax
        Vby = tempVay
        or:
        Vax = Vax + Vbx
        Vbx = Vax - Vbx
        Vax = Vax - Vbx
        Vay = Vay + Vby
        Vby = Vay - Vby
        Vay = Vay - Vby
    }
 
    Game Rules:
    The five balls move in the canvas and they will collide with each other. Of course, the ball will collide with up, down, left and right.
    After the collision, the ball will change direction and return to
    38.The bottom cursor is used to adjust the movement speed of the ball. Cursor The range is [-100, 100]
     
    defects or BUG:
    1. When the cursor data is modified to change the speed of the ball movement, the distance the ball moves is not updated in time
    resulting in the ball may flee the canvas
    2. The ball in the process of the movement, and sometimes it is possible to escape from the canvas.
 
    Summary:
    It took a week to finish the game. In this process, not only did they go back to learning the knowledge of mathematics in high school,
    physical knowledge, many things were forgotten, but soon they learned to return.
    In fact, many games are mathematical problems.
    There are still flaws or bugs in the 49      
    games. Hopefully the like-minded people can improve together.
 '''

__author__ = {'author' : 'Hongten',
              'Email' : 'hongtenzone@foxmail.com',
              'Blog' : 'http://www.cnblogs.com/hongten/',
              'Created' : '2013-09-28',
              'Version' : '1.0'}

class Pong(Frame):
    def createWidgets(self):
        ## Canvas 
        self.draw = Canvas(self, width="5i", height="5i", bg='white')

        ## Cursor(control ball speed,range: [-100, 100])
        self.speed = Scale(self, orient=HORIZONTAL, label="ball speed",from_=-100, to=100)

        self.speed.pack(side=BOTTOM, fill=X)

        # The sphere collides with the wall's range
        self.scaling_right = 4.8
        self.scaling_left = 0.2
        # ball diameter
        self.ball_d = 0.4
        # cursor degree
        self.scale_value = self.speed.get()
        # scaling rate
        self.scaling = 100.0

        # deposit ball Array
        self.balls = []
        # store ball x coordinate array
        self.ball_x = []
        # store ball y coordinate array
        self.ball_y = []
        # store ball x axis speed array
        self.ball_v_x = []
        # store ball y-axis speed array
        self.ball_v_y = []

        # five-ball
        self.ball = self.draw.create_oval("0.10i", "0.10i", "0.50i", "0.50i",fill="red")
        self.second_ball = self.draw.create_oval("0.70i", "0.70i", "1.10i", "1.10i",fill='black')
        self.three_ball = self.draw.create_oval("1.30i", "1.30i", "1.70i", "1.70i",fill='brown')
        self.four_ball = self.draw.create_oval("2.0i", "2.0i", "2.40i", "2.40i",fill='green')
        self.five_ball = self.draw.create_oval("3.0i", "3.0i", "3.40i", "3.40i",fill='gray')

        # the five balls into an array
        self.balls.append(self.ball)
        self.balls.append(self.second_ball)
        self.balls.append(self.three_ball)
        self.balls.append(self.four_ball)
        self.balls.append(self.five_ball)

        # first balls, i.e. the center coordinates self.ball (self.x, self.y), here the scaling, the aim In order to 
        # in the ball movement process is more smooth
        self.x = 0.3        
        self.y = 0.3
        # The first ball speed direction
        self.velocity_x = -0.2
        self.velocity_y = 0.5

        self.second_ball_x = 0.9
        self.second_ball_y = 0.9
        self.second_ball_v_x = 0.4
        self.second_ball_v_y = -0.5

        self.three_ball_x = 1.5
        self.three_ball_y = 1.5
        self.three_ball_v_x = -0.3
        self.three_ball_v_y = -0.5

        self.four_ball_x = 2.2
        self.four_ball_y = 2.2
        self.four_ball_v_x = 0.1
        self.four_ball_v_y = -0.5

        self.five_ball_x = 3.2
        self.five_ball_y = 3.2
        self.five_ball_v_x = 0.3
        self.five_ball_v_y = 0.5

        
        # update ball coordinates
        self.update_ball_x_y()
        self.draw.pack(side=LEFT)

    def update_ball_x_y(self, *args):
        ''' Update the coordinates of the ball, that is, the coordinates of the center point of each ball and the speed 
            information are stored in the array, and is convenient to be used in the subsequent loop traversal. ''' 
         # first ball information
        self.ball_x.append(self.x)
        self.ball_y.append(self.y)
        self.ball_v_x.append(self.velocity_x)
        self.ball_v_y.append(self.velocity_y)

        self.ball_x.append(self.second_ball_x)
        self.ball_y.append(self.second_ball_y)
        self.ball_v_x.append(self.second_ball_v_x)
        self.ball_v_y.append(self.second_ball_v_y)

        self.ball_x.append(self.three_ball_x)
        self.ball_y.append(self.three_ball_y)
        self.ball_v_x.append(self.three_ball_v_x)
        self.ball_v_y.append(self.three_ball_v_y)

        self.ball_x.append(self.four_ball_x)
        self.ball_y.append(self.four_ball_y)
        self.ball_v_x.append(self.four_ball_v_x)
        self.ball_v_y.append(self.four_ball_v_y)

        self.ball_x.append(self.five_ball_x)
        self.ball_y.append(self.five_ball_y)
        self.ball_v_x.append(self.five_ball_v_x)
        self.ball_v_y.append(self.five_ball_v_y)
    
    def update_ball_velocity(self, index, *args):
        '''Update each ball velocity information, i.e., the sides and the ball hits the pellets further speed information update request ''' 
        # cursor values 
        self.scale_value = self.speed.get ()
        # collision wall
        if (self.ball_x[index] > self.scaling_right) or (self.ball_x[index] < self.scaling_left):
            self.ball_v_x[index] = -1.0 * self.ball_v_x[index]
        if (self.ball_y[index] > self.scaling_right) or (self.ball_y[index] < self.scaling_left):
            self.ball_v_y[index] = -1.0 *  self.ball_v_y[index]

        '''
        #TEST:
        for n in range(len(self.balls)):
            #print((self.ball_x[index] - self.ball_x[n])**2)
            #print(round((self.ball_x[index] - self.ball_x[n])**2 + (self.ball_y[index] - self.ball_y[n])**2, 2))
            print(round((self.ball_x[index] - self.ball_x[n])**2 + (self.ball_y[index] - self.ball_y[n])**2, 2) <= round(self.ball_d**2, 2))
        '''
        for n in range(len(self.balls)):
            #pellets crash conditions,namely:(X2-X1)^2+(Y2-Y1)^2<=(R&lt+R&lt)^2 
            if (round((self.ball_x[index] - self.ball_x[n])**2 + (self.ball_y[index] - self.ball_y[n])**2, 2) <= round(self.ball_d**2, 2)):
                #two ball speed exchange
                temp_vx = self.ball_v_x[index]
                temp_vy = self.ball_v_y[index]
                self.ball_v_x[index] = self.ball_v_x[n]
                self.ball_v_y[index] = self.ball_v_y[n]
                self.ball_v_x[n] = temp_vx
                self.ball_v_y[n] = temp_vy
        #print(self.ball_v_x, self.ball_v_y)
               
        '''
        #WRONG:
        for n in range(len(self.balls)):            
            if (((self.ball_x[index] - self.ball_x[n])**2 + (self.ball_y[index] - self.ball_y[n])**2) <= self.ball_d**2):
                #两小球速度交换
                self.ball_v_x[index] = self.ball_v_x[index] + self.ball_v_x[n]
                self.ball_v_x[n] = self.ball_v_x[0] - self.ball_v_x[n]
                self.ball_v_x[index] = self.ball_v_x[index] - self.ball_v_x[n]
                self.ball_v_y[index] = self.ball_v_y[index] + self.ball_v_y[n]
                self.ball_v_y[n] = self.ball_v_y[index] - self.ball_v_y[n]
                self.ball_v_y[index] = self.ball_v_y[index] - self.ball_v_y[n]
        print(self.ball_v_x, self.ball_v_y)
        '''
        
    def get_ball_deltax(self, index, *args):
        '''Obtain pellets X coordinate and a moving distance of the center of the updated X coordinate of the ball, a desired 
        return to the X-axis moving distance'''
        deltax = (self.ball_v_x[index] * self.scale_value / self.scaling)
        self.ball_x[index] = self.ball_x[index] + deltax
        return deltax

    def get_ball_deltay(self, index, *args):
        '''Gets the ball's Y axis coordinate movement distance and updates the ball's center Y coordinate, returns the Y 
        axis's required movement distance'''
        deltay = (self.ball_v_y[index] * self.scale_value / self.scaling)
        self.ball_y[index] = self.ball_y[index] + deltay
        return deltay
    
    def moveBall(self, *args):
        '''Move the first ball , numbered 0, which is determined based on the array: self.balls.'''
        self.update_ball_velocity(0)       
        deltax = self.get_ball_deltax(0)
        deltay = self.get_ball_deltay(0)
        #pellets mobile
        self.draw.move(self.ball,  "%ri" % deltax, "%ri" % deltay)
        self.after(10, self.moveBall)

    def move_second_ball(self, *args):
        self.update_ball_velocity(1)       
        deltax = self.get_ball_deltax(1)
        deltay = self.get_ball_deltay(1)        
        self.draw.move(self.second_ball,  "%ri" % deltax, "%ri" % deltay)
        self.after(10, self.move_second_ball)


    def move_three_ball(self, *args):
        self.update_ball_velocity(2)       
        deltax = self.get_ball_deltax(2)
        deltay = self.get_ball_deltay(2)
        self.draw.move(self.three_ball,  "%ri" % deltax, "%ri" % deltay)
        self.after(10, self.move_three_ball)

    def move_four_ball(self, *args):
        self.update_ball_velocity(3)       
        deltax = self.get_ball_deltax(3)
        deltay = self.get_ball_deltay(3)
        self.draw.move(self.four_ball,  "%ri" % deltax, "%ri" % deltay)
        self.after(10, self.move_four_ball)

    def move_five_ball(self, *args):
        self.update_ball_velocity(4)       
        deltax = self.get_ball_deltax(4)
        deltay = self.get_ball_deltay(4)
        self.draw.move(self.five_ball,  "%ri" % deltax, "%ri" % deltay)
        self.after(10, self.move_five_ball)

            
    def __init__(self, master=None):
        ''' Initialization function '''
        Frame.__init__(self, master)
        Pack.config(self)
        self.createWidgets()
        self.after(10, self.moveBall)
        self.after(10, self.move_three_ball)
        self.after(10, self.move_four_ball)
        self.after(10, self.move_five_ball)
        self.after(10, self.move_second_ball)
        
        
game = Pong()

game.mainloop()