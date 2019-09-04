from tvb.simulator.lab import *
from matplotlib import pyplot as plt
import numpy

from utils import *

print('Loading some connectivities')

conns = {'paupau':get_paupau_conn(), '2regions':get_2_region_conn(weight_between=2), '3regions':get_3_region_conn()}

conns['connectivity_66'] = connectivity.Connectivity.from_file('connectivity_66.zip')

for conn_id in conns:

    conn = conns[conn_id]
    conn.configure()

    conn_info(conn, conn_id)
    
    plot_connectivity(connectivity = conn, plot_tracts=False)
    
    fig = plt.gcf()
    fig.canvas.set_window_title(conn_id)

plt.show()

