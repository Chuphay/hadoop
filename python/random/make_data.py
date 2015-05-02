import sys
from random import gauss, randint 

f = open(sys.argv[1],'w')
def makeData(seed):
    classes = ["Geography", "Math","Science", "Latin","English", "Psychology", "Art", "Music", "History"]
    schools = ["ABC","DEF","GHI","JKL","MNO", "XYZ"]

    mu = seed%100 + 30
    score = gauss(mu, mu/7)
    if(score>100):
        diff = score-100
        score = 100 - diff
    if(score < 0):
        score = -score
    school = schools[randint(0,len(schools)-1)]
    course = classes[randint(0,len(classes)-1)]
    f.write(str(seed)+","+course+"," +school +" University,"+ "2015-04-31,"+ str(round(score))+"\n")
 
for i in range(2000):
    makeData(randint(0,120))
f.close()
