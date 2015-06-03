import sys
import random

test = open("air_test.txt","w")

i,num = 0, 0
for line in sys.stdin:
    i += 1
    if(i == 1):
        continue
    r = random.uniform(0,1)
    if(r<0.0001):
        test.write(line)
        num += 1

print("number of written lines:", num, "out of", i-1)
