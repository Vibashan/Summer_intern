#!/usr/bin/env python

import pylab as plt
from pylab import plot,show, scatter
from scipy.cluster.vq import *
import numpy
import math

plt.figure(1)
xp,yp,xt,yt = 0,50,0,0
for i in range(0,360):
	xe = 50*(2*math.cos(math.radians(i))-math.sin(2*math.radians(i)))
	ye = 50*(math.cos(2*math.radians(i))-2*math.sin(math.radians(i)))
	if (xe-xp) == 0:
		xe = 0.00001
	s = (ye-yp)/(xe-xp)
	ym = (ye+yp)/2
	xm = (xe+xp)/2
	xi = (s*(ym-yt)+(s*s)*xt+xm)/((s*s)+1)
	yi = yt-s*xt+s*xi
	plot(xe, ye, 'or')
	plot(xi, yi, 'ok')
plot(0,0, 'ob')
plot(0,50, 'oy')
plt.axis([-160, 160, -160, 160])
show()