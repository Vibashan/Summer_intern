#!/usr/bin/env python

import pylab as plt
from pylab import plot,show, scatter
from scipy.cluster.vq import *
import numpy
import csv

A = list()
B = list()
C = list()
D = list()

a = list()
b = list()
c = list()
d = list()

def Read(inputfile):
    cnt = 0
    with open(inputfile, 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:

            for i in row:
                #print c, i

                if(cnt%8 == 0) or (cnt%8 == 1):
                    A.append(i)
                if (cnt % 8 == 2) or (cnt % 8 == 3):
                    B.append(i)
                cnt = cnt + 1
    csvFile.close()
    for i in range(len(A)):
        for char in '()':
            j = A[i]
            A[i] = j.replace(char, '')
    A.remove('Ax')
    A.remove('Ay')

    for i in range(len(B)):
        for char in '()':
            j = B[i]
            B[i] = j.replace(char, '')
    B.remove('Bx')
    B.remove('By')

    for i in range(0, len(A), 2):
        (x, y) = (float(A[i]), float(A[i+1]))
        a.append([x, y])

    for i in range(0, len(B), 2):
        (x, y) = (float(B[i]), float(B[i+1]))
        b.append([x, y])

def plotabcd():
    plt.figure(1)
    j = -1
    for i in a:
        j+=1
        if b[j][0] == 0:
            x, y = i[0], i[1]
            plot(x, y, 'or')
        elif b[j][0] == 1:
            x, y = i[0], i[1]
            plot(x, y, 'og')
        elif b[j][0] == 2:
            x, y = i[0], i[1]
            plot(x, y, 'ok')

    plot(700,300, 'ob')
    plot(612,88, 'ob')
    plot(400,300, 'oy')

def main():
    '''
    give the input file name and the no. of clusters to be formed(at_max 8)
    can give more clusters by adding more color points c*
    '''
    inputfile = 'pur_ana_ang_2.csv'
    Read(inputfile)

    plotabcd()
    show()



if __name__ == '__main__':
    main()
