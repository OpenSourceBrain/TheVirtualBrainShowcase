from tvb.simulator.lab import *
import numpy as np
from matplotlib import pyplot as plt


rww = models.ReducedWongWang(a=0.27, w=1.0, I_o=0.3)
S = np.linspace(0, 1, 50).reshape((1, -1, 1))
C = S * 0.0
dS = rww.dfun(S, C)

plt.figure()
plt.plot(S.flat, dS.flat)

plt.show()


