from numpy.random import normal, uniform

#formula y = -3 + 2*x + noise
#range of x will be from -10 t0 10


for i in range(100):
    x = uniform(-10,10)
    y = -3 + 2*x + normal()/5
    print x, y

