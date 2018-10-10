#!/usr/bin/env python

import pylab as plt
from pylab import plot,show, scatter
from scipy.cluster.vq import *
import numpy
import csv
import math


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
                if (cnt % 8 == 6) or (cnt % 8 == 7):
                    D.append(i)
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

    for i in range(len(D)):
        for char in '()':
            j = D[i]
            D[i] = j.replace(char, '')
    D.remove('Dx')
    D.remove('Dy')

    for i in range(0, len(A), 2):
        (x, y) = (float(A[i]), float(A[i+1]))
        a.append([x, y])

    for i in range(0, len(B), 2):
        (x, y) = (float(B[i]), float(B[i+1]))
        b.append([x, y])

    for i in range(0, len(C), 2):
        (x, y) = (float(C[i]), float(C[i+1]))
        c.append([x, y])

    for i in range(0, len(D), 2):
        (x, y) = (float(D[i]), float(D[i+1]))
        d.append([x, y])
    return len(A)

def plot_abcd():
    plt.figure(1)
    for i in a:
        px, py = i[0], i[1]
        plot(x, y, 'or')
    for i in b:
        ex_1, ey_1 = i[0], i[1]
        plot(x, y, 'og')
    for i in c:
        ex_2, ey_2 = i[0], i[1]
        plot(x, y, 'ob')
    for i in d:
        xt, yt = i[0], i[1]
        plot(x, y, 'oy')
        return px,py,ex_1,ey_1,ex_2,ey_2,xt,yt

def get_pts(i):
    p = numpy.array(a)
    e1 = numpy.array(b)
    e2 = numpy.array(c)
    t = numpy.array(d)
    px, py = p[i][0], p[i][1]
    ex_1, ey_1 = e1[i][0], e1[i][1]
    ex_2, ey_2 = e2[i][0], e2[i][1]
    xt, yt = t[i][0], t[i][1]
    return px,py,ex_1,ey_1,ex_2,ey_2,xt,yt



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
    i = 0
    inputfile = 'pur_lose_nor_diff_small_pts.csv'
    max_i = Read(inputfile)
    while(i<(max_i-2)):
        px,py,ex_1,ey_1,ex_2,ey_2,xt,yt = get_pts(i)
        #print 'px-',px,'py-',py,'ex_1-',ex_1,'ey_1-',ey_1,'ex_2-',ex_2,'ey_2-',ey_2,'xt-',xt,'yt-',yt
        d_pt = math.sqrt((px-xt)*(px-xt)+(py-yt)*(py-yt))
        d_e1_t = math.sqrt((ex_1-xt)*(ex_1-xt)+(ey_1-yt)*(ey_1-yt))
        d_e2_t = math.sqrt((ex_2-xt)*(ex_2-xt)+(ey_2-yt)*(ey_2-yt))
        r1 = max(d_e1_t,d_e2_t)
        r2 = min(d_e1_t,d_e2_t)
        print (r2)/r1
        #print 'd_pt-',d_pt,'d_e1_t-',d_e1_t,'d_e2_t-',d_e2_t
        i+=1

if __name__ == '__main__':
    main()
