from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy

def get_default_conn():
    
    conn = connectivity.Connectivity(load_default=True)

    return conn


def get_paupau_conn():
    conn = connectivity.Connectivity.from_file("paupau.zip")

    return conn
    

def get_2_region_conn(weight_between=0):
    conn = connectivity.Connectivity()
    conn.region_labels = numpy.array(['R0', 'R1'])
    conn.weights = numpy.array([[0,weight_between],[0,0]])
    conn.centres = numpy.array([[0,0,0],[5,5,5]])

    return conn


def get_1_region_conn():
    conn = connectivity.Connectivity()
    conn.region_labels = numpy.array(['R0'])
    conn.weights = numpy.array([[0]])
    conn.centres = numpy.array([[0,0,0]])

    return conn



def conn_info(conn):
    print('================= Connection info ===================')
    print('Regions:    %s'%conn.region_labels)
    print('Weights:    %s'%conn.weights)
    print('Undirected: %s'%conn.undirected)
    print('Centres:    %s'%conn.centres)
    print('=====================================================')
    
    
def data_info(data):
    print('=================== Data info =======================')
    print('Data %s, shape: %s, %s: %s -> %s'%(type(data), data.shape, len(data), data[0],data[-1]))
    print('=====================================================')
    

def run_model(model, connectivity, duration, dt=0.01, coupling_linear=0, initial_conditions=None):

    #heunstochint = integrators.HeunStochastic()
    integ = integrators.HeunDeterministic(dt=dt)

    sim = simulator.Simulator(
        model = model, 
        connectivity = connectivity,
        coupling = coupling.Linear(a=coupling_linear), 
        integrator = integ, 
        initial_conditions = initial_conditions,
        monitors = monitors.Raw(),
        simulation_length=duration,
    ).configure()

    #print sim.history

    # run
    result = sim.run()
    
    (tavg_time, tavg_data), = result

    data_info(tavg_time)
    data_info(tavg_data)

    # plot
    plt.figure()

    for i in range(len(tavg_data[0][0])):
        for j, var in enumerate(model.variables_of_interest):
            print('Adding plot for region %i, variable %i %s'%(i, j, var))
            plt.plot(tavg_time, tavg_data[:, j, i, 0], label = 'R%i_%s'%(i,var), alpha=0.4)

    plt.grid(True)
    plt.legend()
    plt.xlabel('Time (ms)')
    plt.ylabel("Variables")


    