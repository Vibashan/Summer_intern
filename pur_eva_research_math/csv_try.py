#!/usr/bin/env python
import numpy as np
import csv
'''
filename = 'csv_try.csv'

def writecsv(req,condi):
    global filename
    file = open(filename,'a')
    datastr = "," + str(req)   		#"," + color + "-" + shape + "-" + str(cx) + "-" + str(cy)
    file.write(datastr)
    if condi == 1:
    	file.write

csv = open(filename, "w")
a = 5,2,5,6,8,2
a = np.asarray(a)
b = np.arange(100)
columnTitleRow = str(a)+","+str(b)
csv.write(","+columnTitleRow) '''

'''import os
from os.path import expanduser

home = expanduser('~')
a = (5,6,3,4,5,61)
a =str(a)

dl_path = home + '/trail'

def main():
    if not os.path.exists(dl_path):
       print ("path doesn't exist. trying to make")
       os.makedirs(dl_path)'''
a = (5,6,3,4,5,61)
a =str(a)       
outfile = a
speed=np.arange(10)
f1=open(outfile+".txt","w+")
f1.write((str)(speed))
f1.write("\n")
b=np.arange(2000)
for i in range(b.size):
	f1.write((str)(b[i]))
	f1.write("\n")

 # X is an array
#np.savetxt('test.out', (x,y,z))   # x,y,z equal sized 1D arrays
#np.savetxt('test.out', x, fmt='%1.4e')   # use exponential notation

