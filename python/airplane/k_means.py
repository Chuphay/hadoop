############################################
#
#python k_means.py air_test.txt < 1987.csv 
#
###########################################


import sys
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



test_data = []
for d in test_file:

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



i,error = 0,0
weights = [1 for i in range(12)]
weights[11] = 0.0
output = [[(20000,"None",None)] for i in range(len(test_data))]
#print ("Starting....")
for line in sys.stdin:
    i += 1

    if(i == 1):
        #pass over the header
        continue

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
            output[k] = (sorted(output[k]))[:22]
        

    except ValueError:
        ###print(line)
        error += 1

        
print(i,error)
