import sys,re

j,errors = 0,0
correct, total = 0,0
prob = 0.5
for i,line in enumerate(sys.stdin):
    s = re.match("^Cannot process this", line) #couldn't process this entry
    if(s):
        errors += 1
        continue
    target = re.match("^\(0.0, (-?\d+)\)", line) #looking for a target
    knn_average = re.match("^\d.\d+",line)
    if(target):
        myTarget = target.group(1)
        #print("target", myTarget)
        temp_data = []
        j = 0
        total += 1
    elif(knn_average):
        score =  knn_average.group()
        #print("knn_average",score)
        if((float(score)>= prob) and (int(myTarget)>=15)):
            correct += 1
        elif((float(score)< prob) and (int(myTarget)<15)):
            correct += 1
        else:
            
            delay = []
            for t in temp_data:
                d = re.search(", (-?\d+)", t).group(1)
                delay.append(int(d))
                print(t.strip())
            print ("Incorrect: ",myTarget, score)
            print("median: ",sorted(delay)[10])
    else:
        j += 1
        if(j>21):
            print("error, j is more than 21", j)
        temp_data.append(line)

    
        
    #print(i, line.strip())
    #if(i>100):
    #    break

print("correct", correct, "total", total, "percent correct", float(correct)/total)
print("not important errors", errors)
