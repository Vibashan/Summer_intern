#!/usr/bin/env python

import math

(x_t,y_t) = (10,0)
(x_1,y_1) = (6,0.5)
if abs(y_t-y_1) < 5 and abs(x_t-x_1) <5:
	print('i am here')

print(math.atan2(math.sin(math.pi*(180-0)/180),math.cos(math.pi*(180-0)/180)))
print((180*0.1)/(math.pi))
print(math.degrees(math.atan((y_t-y_1)/(x_t-x_1))))
print(math.degrees(math.atan2((y_t-y_1),(x_t-x_1))))
print(math.sqrt((x_t-x_1)**2+(y_t-y_1)**2))