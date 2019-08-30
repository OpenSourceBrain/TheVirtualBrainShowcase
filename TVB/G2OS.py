from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy
from utils import *


model = models.Generic2dOscillator()
#oscillator.a = -2
#oscillator.tau = 1

model.configure()


conn = get_2_region_conn(weight_between=1)


run_model(model, conn, 200, coupling_linear=0.01)

plt.show()


plt.show()

