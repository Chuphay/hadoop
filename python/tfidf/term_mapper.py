import sys


data = {}
for line in sys.stdin:
    word, file_name, num = line.split()
    try:
        data[word][file_name] = num
    except KeyError:
        data[word] = {file_name:num}

for word in data:
    out = [word]
    for file_name in data[word]:
        out.append(file_name)
        out.append(data[word][file_name])
    out = " ".join(out)
    print out 

    
