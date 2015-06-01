####################################################################
#
#python do_something.py < 1987_top1000.csv
#
#now it works more like this:
#
#python do_something.py air_test.txt < airline_1987.csv 
#
####################################################################
header = """
Year,Month,DayofMonth,DayOfWeek,DepTime,CRSDepTime,ArrTime,CRSArrTime,UniqueCarrier,FlightNum,TailNum,ActualElapsedTime,CRSElapsedTime,AirTime,ArrDelay,DepDelay,Origin,Dest,Distance,TaxiIn,TaxiOut,Cancelled,CancellationCode,Diverted,CarrierDelay,WeatherDelay,NASDelay,SecurityDelay,LateAircraftDelay
"""
###print(header)
sample = """1987,10,14,3,741,730,912,849,PS,1451,NA,91,79,NA,23,11,SAN,SFO,447,NA,NA,0,NA,0,NA,NA,NA,NA,NA"""
sample2 = """1987,10,12,1,631,630,731,727,PS,1503,NA,60,57,NA,4,1,LAX,SJC,308,NA,NA,0,NA,0,NA,NA,NA,NA,NA"""
sample3 = """1987,10,30,5,1950,1930,2103,2040,PS,1502,NA,73,70,NA,23,20,SMF,LAX,373,NA,NA,0,NA,0,NA,NA,NA,NA,NA"""
import sys
if(len(sys.argv) != 2):
    print "have to supply a test file"
    sys.exit(1)
test_file  = open(sys.argv[1]).readlines()
#print test_file

#I want to keep
#Year, Month, DayofMonth, DayOfWeek, CRSDepTime, CRSArrTime, UniqueCarrier
#0   , 1    ,    2      ,   3      ,     5     ,   7       ,     8
#FlightNum, CRSElapsedTime, DepDelay, Origin, Dest
#  9      ,      12       ,   15    ,  16   ,  17
#target: ArrDelay
#14

#numeric: 5, 7, 12, 15 :=> 14
#categorical: 0, 1, 2, 3, 8, 9, 16, 17 :=> is(ArrDelay>15)? category 1 or 0
#Now that I think about it, I would rather have, CRSDepTime and CRSArrTime 
#to be categorical as well
#So we will put a cutoff, like within 30 minutes is considered the same category
#so, now numeric simply consists of 15 :=> 14
#and categorical: 0, 1, 2, 3, 8, 9,12, 16, 17, 5<30 min, 7<30 min :=> 15<ArrDelay

#Let's use Jacard's similarity condition for the categorical data
def get_distance(weights, data):
    """Data should come in the following format:
    year, month, dayofMonth, dayOfWeek, CRSDepTime, 
    CRSArrTime, UniqueCarrier, flightNum,  Origin, Dest, 
    CRSElapsedTime, DepDelay"""
    assert(len(weights) == len(data)==12), "Yo!"
    #first deal with the categorical stuff
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
    ###print(jaccard, weights[11]*data[11])
    return  jaccard+weights[11]*data[11] 
test_data = []
for d in test_file:
    #print "yo", data
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

#import sys
i,error = 0,0
weights = [1 for i in range(12)]
weights[11] = 0.05
output = [[(20000,"None",None)] for i in range(len(test_data))]
#print ("Starting....")
for line in sys.stdin:
    i += 1
    #print(i)
    if(i == 1):
        #pass over the header
        continue
    #if(i%100 == 0):
    #    print(i)
    #    continue
    ###print(line)

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

        
#print(i,error)
for i in output:
    delay, nums = 0,0
    for o in i:
        print(o)
        if(o[0] == 0):
            continue
        nums += 1
        delay += (o[1]>15)
    print (float(delay)/ float(nums)) 




