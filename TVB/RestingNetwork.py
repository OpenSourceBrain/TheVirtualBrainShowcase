# Based on https://nbviewer.jupyter.org/url/docs.thevirtualbrain.org/tutorials/tutorial_s5_ModelingRestingStateNetworks.ipynb

from tvb.simulator.lab import *

import time
import numpy

from utils import *
from matplotlib import pyplot as plt

model=models.Generic2dOscillator(a=0.0)

def run_sim(conn, cs, D, cv=3.0, dt=0.5, simlen=1e3):
    sim = simulator.Simulator(
        model=model,
        connectivity=conn,
        coupling=coupling.Linear(a=cs),
        integrator=integrators.HeunStochastic(dt=dt, noise=noise.Additive(nsig=numpy.array([D]))),
        monitors=monitors.TemporalAverage(period=5.0) # 200 Hz
    )
    sim.configure()
    print("Starting simulation of duration %sms (dt=%sms)"%(simlen,dt))
    (t, y), = sim.run(simulation_length=simlen)
    return t, y[:, 0, :, 0]

conn = connectivity.Connectivity(load_default=True)
#conn = get_2_region_conn(weight_between=1)

tic = time.time()
t, y = run_sim(conn, 6e-2, 5e-4, simlen=5000)


data_info(t)
data_info(y)

print('simulation required %0.3f seconds.' % (time.time() - tic, ))


plt.figure()

for i in range(len(y[0])):
    #for j, var in enumerate(model.variables_of_interest):
    var = 'vvv'
    print('Adding plot for region %i, variable %s %s'%(i, '?', '?'))
    plt.plot(t, y[:,i], label = 'R%i_%s'%(i,var), alpha=0.4)

plt.grid(True)
plt.legend()
plt.xlabel('Time (ms)')
plt.ylabel("Variables")

plt.show()

