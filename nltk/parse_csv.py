myFile = open("annotated.csv").readlines()

data = []
i = 0
for line in myFile:
    if line[0] == '[':
        i += 1
        line = line.replace(",,","")        
        line = line.replace("[,","")
        line = line.replace(",]","")
        line = line.replace("'","")
        line = line.strip()
        split_line = line.split(",")
        l = len(split_line)
        if(l%2 != 0):
            print "error!!!"
        temp = [] 
        for j in range(int(l/2)): #python 2/3 hack
            temp.append((split_line[j],split_line[j+1]))
            
        data.append(temp)
    else:
        pass


print data

