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
                if (cnt % 8 == 4) or (cnt % 8 == 5):
                    C.append(i)
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

    for i in range(len(C)):
        for char in '()':
            j = C[i]
            C[i] = j.replace(char, '')
    C.remove('Cx')
    C.remove('Cy')

    for i in range(0, len(A), 2):
        (x, y) = (float(A[i]), float(A[i+1]))
        a.append([x, y])

    for i in range(0, len(B), 2):
        (x, y) = (float(B[i]), float(B[i+1]))
        b.append([x, y])

    for i in range(0, len(C), 2):
        (x, y) = (float(C[i]), float(C[i+1]))
        c.append([x, y])

def plotabcd():
    plt.figure(1)
    for i in a:
        x, y = i[0], i[1]
        plot(x, y, 'or')
    for i in b:
        x, y = i[0], i[1]
        plot(x, y, 'og')
    for i in c:
        x, y = i[0], i[1]
        plot(x, y, 'ob')

    plot(0+400,0+300, 'ob')
    plot(1+400,-190+300, 'oc')
    plot(50+400,-70+300, 'ok')
    plt.axis([0, 1000, 0, 1000])


def main():
    '''
	give the input file name and the no. of clusters to be formed(at_max 8)
	can give more clusters by adding more color points
    '''
    inputfile = 'E2_set_pts_analysis.csv'
    Read(inputfile)

    plotabcd()
    show()



if __name__ == '__main__':
    main()
