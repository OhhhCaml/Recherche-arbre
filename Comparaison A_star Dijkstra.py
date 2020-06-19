import Dijkstra
import A_star
import Grib
import time
import numpy as np
import force_to_temps as ftt
from math import *


grib = Grib.Grib()
n = 10

x = np.random.randint(0,71,(n,2))
y = np.random.randint(0,151,(n,2))



def heuristique1(c1):
    a = c1.dernier_point()
    arrivee = c1.arrivee()
    i = abs(a[0] - arrivee[0])
    j = abs(a[1] - arrivee[1])
    return(ftt.force_to_temps(c1.u()*i + j*c1.v()))

def heuristique2(c1):
    return(0)

t1 = time.time()
for i in range(n):
    A_star.A_star(grib,(x[i][0],y[i][0]),(x[i][1],y[i][1]),heuristique1)
print((time.time()-t1)/n)

t1 = time.time()
for i in range(n):
    A_star.A_star(grib,(x[i][0],y[i][0]),(x[i][1],y[i][1]), heuristique2)
print((time.time() - t1)/n)


t1 = time.time()
for i in range(n):
    Dijkstra.dijkstra(grib,(x[i][0],y[i][0]),(x[i][1],y[i][1]))
print((time.time()-t1)/n)

