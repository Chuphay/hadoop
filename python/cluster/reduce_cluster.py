import sys

data = {}
num_clusters_start = 0
for line in sys.stdin:
    words = line.split()
    if(words[2] == 'in'):
        print(line)

