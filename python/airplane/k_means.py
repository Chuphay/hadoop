############################################
#
#python k_means.py air_test_small.txt < 1987.csv 
#
###########################################


import sys
import random

if(len(sys.argv) != 2):
    print( "have to supply a test file")
    sys.exit(1)
test_file  = open(sys.argv[1]).readlines()

def get_distance(weights, data):
    """Data should come in the following format:
    year, month, dayofMonth, dayOfWeek, CRSDepTime, 
    CRSArrTime, UniqueCarrier, flightNum,  Origin, Dest, 
    CRSElapsedTime, DepDelay"""

    assert(len(weights) == len(data)==12), "Yo!"

    jaccard_numerator  = 0
    jaccard_denom = 0

    #We will use the standard Jaccard, where not_same/(num_of_tests)
    for i in range(11):
        jaccard_denom += weights[i]
        if(data[i] == 0):
            jaccard_numerator += weights[i]
        elif(data[i] == 1): 
            pass
        else:
            print("something terrible happened")

    jaccard = float(jaccard_numerator)/float(jaccard_denom)

    return  jaccard+weights[11]*data[11]


def get_tot_distance(tot_data, test_center, c):
    dist = 0
    for i,line in enumerate(tot_data):
        if(clusters[i] != c):
            continue
        words = line.split(",")
        word_test = test_center.split(",")

        data = [0 for j in range(12)]
        data[0] = (int(words[0]) == int(word_test[0]))
        data[1] = (int(words[1]) == int(word_test[1]))
        data[2] = (int(words[2]) == int(word_test[2]))
        data[3] = (int(words[3]) == int(word_test[1]))
        data[4] = (abs(int(words[5]) - int(word_test[5]))<30)
        data[5] = (abs(int(words[7]) - int(word_test[7]))<30)
        data[6] = (words[8] == word_test[8])
        data[7] = (int(words[9]) == int(word_test[9]))
        data[8] = (words[16] == word_test[16])
        data[9] = (words[17] == word_test[17])
        data[10] = (abs(int(words[12]) - int(word_test[12]))<30)
        data[11] = abs(int(words[15]) - int(word_test[15]))
        target = int(words[14])
        dist += get_distance(weights,data)
    return dist





test_data = []
test_data_original = []
for d in test_file:
    test_data_original.append(d)
    s =d.split(",")
    try:
        year = int(s[0])
        month = int(s[1])
        dayofMonth = int(s[2])
        dayofWeek = int(s[3])
        crsDepTime = int(s[5])
        crsArrTime = int(s[7])
        uniqueCarrier = s[8]
        flightNum = int(s[9])
        crsElapsedTime = int(s[12])
        depDelay = int(s[15])
        origin = s[16]
        dest = s[17]
        target = int(s[14])
        test_data.append([year, month, dayofMonth, dayofWeek, crsDepTime, crsArrTime, uniqueCarrier, flightNum, crsElapsedTime, depDelay, origin, dest])
    except ValueError:
        print("Cannot process this: ", s)
        #sys.exit(1)

num_clusters = len(test_data)
print("Number of clusters:", num_clusters) 


i,error = 0,0
weights = [1 for i in range(12)]
weights[11] = 2.5
output = [[] for i in range(len(test_data))]
tot_data = []
#print ("Starting....")





for line in sys.stdin:
    i += 1

    if(i == 1):
        #pass over the header
        continue

    #tot_data.append(line)

    words = line.split(",")

    try:
        #[year, month, dayofMonth, dayofWeek, crsDepTime, crsArrTime, uniqueCarrier,flightNum, crsElapsedTime, depDelay, origin, dest]
        for k,d in enumerate(test_data):
            data = [0 for j in range(12)]
            year = int(words[0])
            data[0] = (year == d[0])
            month = int(words[1])
            data[1] = (month == d[1])
            dayofMonth = int(words[2])
            data[2] = (dayofMonth == d[2])
            dayofWeek = int(words[3])
            data[3] = (dayofWeek == d[3])
            crsDepTime = int(words[5])
            data[4] = (abs(crsDepTime - d[4])<30)
            crsArrTime = int(words[7])
            data[5] = (abs(crsArrTime - d[5])<30)
            uniqueCarrier = words[8]
            data[6] = (uniqueCarrier == d[6])
            flightNum = int(words[9])
            data[7] = (flightNum == d[7])
            origin = words[16]
            data[8] = (origin == d[10])
            dest = words[17]
            data[9] = (dest == d[11])
            crsElapsedTime = int(words[12])
            data[10] = (abs(crsElapsedTime - d[8])<30)
            depDelay = int(words[15])
            data[11] = abs(depDelay - d[9])
            target = int(words[14])
            dist = get_distance(weights,data)

            output[k].append((dist, target))
        tot_data.append(line)

    except ValueError:
        ###print(line)
        error += 1

SSE = [0 for i in range(len(output))]
j = 0
clusters = [0 for i in range(len(output[0]))]
counts = [0 for i in range(len(output))]
for j in range(len(output[0])):
    dist = 100.1
    for k in range(len(output)):
        if(output[k][j][0] < dist):
            clusters[j] = k+1
            dist = output[k][j][0]
        elif(output[k][j][0] == dist):
            if(random.uniform(0,1) < 1.0/len(output)):
                clusters[j] = k+1
    SSE[clusters[j]-1] += dist
    counts[clusters[j] -1] += 1
            
        

print(sum(SSE), counts)
#print(i,j,error, sum(SSE),counts, len(tot_data))

for i in range(len(output)):
    x = 0
    while True:
        x += 1
        #print("x" ,x)
        if(x>3):
            print(test_data_original[i].strip())
            break
        try_this = random.randint(0,counts[i]-1)
        for j,c in enumerate(clusters):
            if(c == i+1):
                if(try_this == 0):
                    new_dist = get_tot_distance(tot_data,tot_data[j],i+1)
                    #print(new_dist)
                    if(new_dist < 1.2*SSE[i]):
                        SSE[i] = new_dist
                        test_data_original[i] = tot_data[j]
                    break
                else:
                    #print(try_this)
                    try_this -= 1
                    


