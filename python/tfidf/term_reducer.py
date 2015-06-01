import sys


data = {}
for line in sys.stdin:
    word, file_name, num = line.split()
    try:
        data[word].append(file_name)
    except KeyError:
        data[word] = [file_name]

for i in data:
    print i, data[i]

    
