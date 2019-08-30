from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy

def conn_info(conn):
    print('====================================')
    print(conn.region_labels)
    print(conn.weights)
    print(conn.undirected)
    print(conn.centres)
    print('====================================')

print('Loading some connectivities')

conn = connectivity.Connectivity(load_default=True)
conn = connectivity.Connectivity()

print(dir(conn))

conn.region_labels = numpy.array(['p1', 'p2'])
conn.weights = numpy.array([[1,1],[0,0]])
conn.centres = numpy.array([[0,0,0],[5,5,5]])

conn_info(conn)

#conn = connectivity.Connectivity.from_file("paupau.zip")

conn_info(conn)

conn.configure()

conn_info(conn)


plot_connectivity(connectivity = conn)

plt.show()

