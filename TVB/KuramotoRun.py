from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy

from utils import *


model = models.Kuramoto()
model.omega = 1
model.configure()

print('Model info: %s'%model)
print(dir(model))
print(model.trait)
print(model.omega)
print(model.observe)
print(model.variables_of_interest)
#print(model.initial([2],[3]))

conn = get_2_region_conn(weight_between=0)

initial_conditions = numpy.array([[[[5],[10]]]])
data_info(initial_conditions)

run_model(model, conn, 100, coupling_linear=0.01, initial_conditions =initial_conditions )

plt.show()
