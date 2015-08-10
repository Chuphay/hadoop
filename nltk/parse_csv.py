myFile = open("annotated.csv").readlines()

data = {}
i = 0
for line in myFile:
    print(line)
    if line[0] == '[':
        i += 1
        line = line.replace(",,","")        
        line = line.replace("[,","")
        line = line.replace(",]","")
        line = line.strip()
        l = line.split(",")
        data[i] = l
    else:
        pass
print( data)

