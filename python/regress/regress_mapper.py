import numpy as np

#x = np.array([1,1])
#a = np.array([[3,6],[6,14]])
#print a
#print np.linalg.inv(a)
#print np.outer(x, np.transpose(x))

import sys

x = []
y = []
for line in sys.stdin:
    temp = line.split()
    x.append(float(temp[0]))
    y.append(float(temp[1]))

x = np.array([np.ones(len(x)),x]).T


A = np.array([[0,0],[0,0]])
B = np.array([0,0])
for i in range(len(y)):
    A += np.outer(x[i], x[i].T)
    B += y[i]*x[i].T

print A[0][0], A[0][1], A[1][0], A[1][1], B[0], B[1]

