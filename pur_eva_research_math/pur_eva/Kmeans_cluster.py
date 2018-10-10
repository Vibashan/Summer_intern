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


def main():
    '''
	give the input file name and the no. of clusters to be formed(at_max 8)
	can give more clusters by adding more color points
    '''
    inputfile = '1.csv'
    Read(inputfile)
    k = raw_input('How many clusters to form:')
    k = int(k)
    data = numpy.concatenate((a, b, c, d))
    res, idx = kmeans2(numpy.array(zip(data[:, 0], data[:, 1])), k)

    colors = ([([0.4, 1, 0.4], [1, 0.4, 0.4], [0.1, 0.8, 1], [0.7, 0.2, 1], [0, 0, 0], [0.3, 0, 0.7], [1, 0.3, 0], [0.5, 0.4, 0.8])[i] for i in idx])
    scatter(data[:, 0], data[:, 1], c=colors)

    # mark centroids
    scatter(res[:, 0], res[:, 1], marker='o', s=500, linewidths=2, c='none')
    scatter(res[:, 0], res[:, 1], marker='x', s=500, linewidths=2)
    print res
    show()


if __name__ == '__main__':
    main()
