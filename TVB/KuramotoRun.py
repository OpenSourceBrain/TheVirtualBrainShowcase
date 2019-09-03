from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy

from utils import *


model = models.Kuramoto()
model.omega = 1
model.configure()

model.configure()
model_info(model)

conn = get_2_region_conn(weight_between=0)

initial_conditions = numpy.array([[[[5],[10]]]])

data_info(initial_conditions)

run_model(model, conn, 100, coupling_linear=0.01, initial_conditions =initial_conditions )

plt.show()
