import sys
import re
data = {}
data_nodes = {}
current_file = None
current_cluster = None
num_clusters_start = 0
for line in sys.stdin:
    print(line.strip())
    x = re.search("file.\.txt", line).group()
    words = line.split()
    num_clusters_start += 1
    nodes = [int(i) for i in re.search("nodes \[(.*)\] per", line).group(1).split(",")]
    for i in nodes:
        data_nodes[i] = num_clusters_start
    perimeter = [int(i) for i in re.search("perimeter \[(.*)\]$",line).group(1).split(",") if i != ""]
    data[num_clusters_start] = {'nodes':nodes, 'area': words[2], 'perimeter':perimeter}

print(data)
print(data_nodes)
num_clusters = 0
for cluster in data:
    print(cluster)
    
