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
                cnt = cnt + 1
    csvFile.close()
    for i in range(len(A)):
        for char in '()':
            j = A[i]
            A[i] = j.replace(char, '')
    A.remove('Ax')
    A.remove('Ay')

    for i in range(0, len(A), 2):
        (x, y) = (float(A[i]), float(A[i+1]))
        a.append([x, y])

def plotabcd():
    plt.figure(1)
    for i in a:
        x, y = i[0], i[1]
        plot(x, y, 'or')
    
    plot(0+400,0+300, 'ob')
    plot(1+400,-190+300, 'og')
    plot(1+400,-250+300, 'og')
    plot(50+400,-70+300, 'oy')
    plot(150+400,-70+300, 'oy')
    plt.axis([0, 1000, 0, 1000])


def kmean(k):
    plt.figure(2)
    data = numpy.concatenate((a, b, c, d))
    res, idx = kmeans2(numpy.array(zip(data[:, 0], data[:, 1])), k)

    colors = ([([0.4, 1, 0.4], [1, 0.4, 0.4], [0.1, 0.8, 1], [0.7, 0.2, 1], [0, 0, 0], [0.3, 0, 0.7], [1, 0.3, 0], [0.5, 0.4, 0.8])[i] for i in idx])
    scatter(data[:, 0], data[:, 1], c=colors)

    # mark centroids
    scatter(res[:, 0], res[:, 1], marker='o', s=500, linewidths=2, c='none')
    scatter(res[:, 0], res[:, 1], marker='x', s=500, linewidths=2)

def main():
    '''
    give the input file name and the no. of clusters to be formed(at_max 8)
    can give more clusters by adding more color points
    '''
    inputfile = 'eva_strt_pts.csv'
    Read(inputfile)

    plotabcd()
    show()



if __name__ == '__main__':
    main()
