from tvb.simulator.lab import models
import numpy as np
from matplotlib import pyplot as plt

print('Creating RWW')

rww = models.ReducedWongWang(a=0.27, w=1.0, I_o=0.3)
print('RWW: %s'%rww)


S = np.linspace(0, 1, 50).reshape((1, -1, 1))
C = S * 0.0
dS = rww.dfun(S, C)

import sys
if not '-nogui' in sys.argv:

    plt.figure()
    plt.plot(S.flat, dS.flat)

    plt.show()

print('Done!')
