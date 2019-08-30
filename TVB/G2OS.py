from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy


oscillator = models.Generic2dOscillator()
#oscillator.a = -2
#oscillator.tau = 1

print dir(oscillator)
print oscillator.summary_info

#exit()

heunstochint = integrators.HeunStochastic(dt=2**-5)
integ = integrators.HeunDeterministic()

# examine integrator's attributes
print heunstochint


conn = connectivity.Connectivity(load_default=True)
conn = connectivity.Connectivity.from_file("paupau.zip")

conn = connectivity.Connectivity()
conn.region_labels = numpy.array(['p1', 'p2'])
conn.weights = numpy.array([[1,1],[0,0]])
conn.centres = numpy.array([[0,0,0],[5,5,5]])

conn.region_labels = numpy.array(['p1'])
conn.weights = numpy.array([[0]])
conn.centres = numpy.array([[0,0,0]])

initial_conditions = numpy.array([[2, 1]])


sim = simulator.Simulator(
    model = oscillator, 
    connectivity = conn,
    coupling = coupling.Linear(a=0.0005), 
    integrator = integ, 
    monitors = monitors.Raw(),
    simulation_length=300,
).configure()

print sim.history

# run
(tavg_time, tavg_data), = sim.run()

print '---------------'
print tavg_time
print '---------------'
print tavg_data
print '---------------'

# plot
plt.figure()
plt.plot(tavg_time, tavg_data[:, 0, :, 0], alpha=0.4)
plt.grid(True)
plt.xlabel('Time (ms)')
plt.ylabel("Temporal average")

plt.show()

