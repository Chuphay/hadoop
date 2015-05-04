import numpy as np
import sys

A = np.array([[0,0],[0,0]])
B = np.array([0,0])

for line in sys.stdin:
    temp = [float(x) for x in line.split()]
    tempA = np.array([[temp[0], temp[1]],[temp[2], temp[3]]])
    tempB = np.array([temp[4], temp[5]])
    #print tempA
    A += tempA
    B += tempB

#print A
#print B
A_inverse = np.linalg.inv(A)
out = np.dot(A_inverse, B)
print out

                     
