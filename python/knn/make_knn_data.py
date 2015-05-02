import numpy as np

a = np.random.normal((5,-10),(2,2),(50,2))
b = np.random.normal((-5,5),(2,2),(50,2))
c = np.random.normal((-8,-4),(2,2),(50,2))

for i in range(50):
    print a[i][0], a[i][1], 'a'
    print b[i][0], b[i][1], 'b'
    print c[i][0], c[i][1], 'c'
