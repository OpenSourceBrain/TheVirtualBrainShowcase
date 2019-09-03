from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy
from utils import *


model = models.Generic2dOscillator(variables_of_interest=['V','W'])
#oscillator.a = -2
#oscillator.tau = 1

model.configure()
print(dir(model))
print(model.state_variables)
print(model.trait)
print(model.variables_of_interest)


conn = get_2_region_conn(weight_between=1)
conn = get_1_region_conn()

initial_conditions = numpy.array([[[[1.5]],[[.4]]]])
initial_conditions = numpy.array([[[[0]],[[-1]]]])
#data_info(initial_conditions)

run_model(model, conn, 1000, coupling_linear=0.0, initial_conditions=initial_conditions)

plt.show()


plt.show()

