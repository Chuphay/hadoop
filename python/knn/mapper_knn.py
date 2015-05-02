import sys

if(len(sys.argv) == 4):
 
    x = float(sys.argv[1])
    y = float(sys.argv[2])
    k = int(sys.argv[3])
else:
    x = 0
    y = 0
    k = 3

distances = []
category = [] 

def distance(x_in, y_in):
    return ((x_in-x)**2 + (y_in - y)**2)**0.5

for line in sys.stdin:
    line = line.strip()
    words = line.split()
    x_in = float(words[0])
    y_in = float(words[1])
    dist = distance(x_in, y_in)
    distances.append(dist)
    category.append(words[2])

out = sorted(zip(distances, category))

for i in range(k):
    print out[i][0], out[i][1]
    #for word in enumerate(words):
    #    print(word+"\t"+str(i))
