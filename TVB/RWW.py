# Based on https://github.com/the-virtual-brain/tvb-root/blob/master/tvb_documentation/demos/simulate_reduced_wong_wang.ipynb
from tvb.simulator.lab import *

import numpy
from matplotlib import pyplot as plt

print('Creating RWW')
'''
rww = models.ReducedWongWang(a=numpy.array([0.27]), w=numpy.array([1.0]), I_o=numpy.array([0.3]))
S = linspace(0, 1, 50).reshape((1, -1, 1))
C = S * 0.0
dS = rww.dfun(S, C)

figure()
plot(S.flat, dS.flat)
'''

rww = models.ReducedWongWang(a=numpy.array([0.27]), w=numpy.array([1.0]), I_o=numpy.array([0.3]))

print('RWW created: %s'%rww)


S = numpy.linspace(0, 1, 50).reshape((1, -1, 1))
C = S * 0.0
dS = rww.dfun(S, C)

import sys
if not '-nogui' in sys.argv:

    plt.figure()
    plt.plot(S.flat, dS.flat)

    plt.show()

print('Done!')
