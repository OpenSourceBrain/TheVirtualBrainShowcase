from tvb.simulator.lab import *
from matplotlib import pyplot as plt

from utils import *

model = models.JansenRit()

model.configure()
model_info(model)

conn = get_2_region_conn(weight_between=1)
conn = get_1_region_conn()

initial_conditions = get_initial_conditions( [0,0,0,0,0,0] , len(conn.region_labels))

run_model(model, conn, 1000, coupling_linear=numpy.array([0.0]), initial_conditions=initial_conditions)

plt.show()
