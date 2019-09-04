
import tables   # pytables for HDF5 support
import os

from neuroml.hdf5.NetworkContainer import *
from neuromllite.BaseTypes import NetworkReader

from neuromllite.utils import print_v
import random

class TVBReader(NetworkReader):
    
    component_objects = {} # Store cell ids vs objects, e.g. NeuroML2 based object
    
    def __init__(self, model, conn, **parameters):
                     
        print_v("Creating TVBReader with %s..."%parameters)
        self.parameters = parameters
        self.model = model
        self.conn = conn
        

    def parse(self, handler):

        if 'id' in self.parameters:
            id = self.parameters['id']
        
        self.handler = handler
    
        notes = "Network from TVB: %s"%'??'
        handler.handle_document_start(id, notes)
        
        handler.handle_network(id, notes)
        
        self.parse_conn()
        
    def parse_conn(self):

        for ri in range(len(conn.region_labels)):
            #print
            pop_id = conn.region_labels[ri]
            component = 'g2do0'
            color = '%s %s %s'%(random.random(),random.random(),random.random())
      
            properties={'color':color, 'radius':5000}
            
            self.handler.handle_population(pop_id, 
                                           component, 
                                           1,
                                           properties=properties)
            centre = conn.centres[ri]
            
            print('Adding population %s at %s properties %s'%(pop_id,centre,properties))
            
            self.handler.handle_location(0, 
                                         pop_id, 
                                         component, 
                                         float(centre[0])*1000, 
                                         float(centre[1])*1000, 
                                         float(centre[2])*1000)
                                         
        print conn.weights
        W = conn.weights
        pre_indices = range(len(W[0]))
        post_indices = range(len(W[0]))
        for pre in pre_indices:
            for post in post_indices:
                pre_pop =  conn.region_labels[pre]
                post_pop = conn.region_labels[post]
                weight = W[pre][post]
                if weight>0:
                    synapse = 'dummy'
                    print("Connecting %s -> %s, %s, %s"%(pre_pop,post_pop, weight,weight>0))
                    
                    proj_id = 'Proj__%s__%s'%(pre_pop,post_pop)
                    self.handler.handle_projection(proj_id, 
                                         pre_pop, 
                                         post_pop, 
                                         synapse)

                    delay = 0
                    
                    self.handler.handle_connection(proj_id, 
                                     0, 
                                     pre_pop, 
                                     post_pop, 
                                     synapse, \
                                     0, \
                                     0, \
                                     delay = delay, \
                                     weight = weight)
    
                    self.handler.finalise_projection(proj_id, 
                                         self.pre_pop, 
                                         self.post_pop, 
                                         synapse)
            

        
    
if __name__ == '__main__':

    from tvb.simulator.lab import *

    from utils import *
    
    model = models.Kuramoto()
    
    conn = get_2_region_conn(weight_between=0)
    conn = connectivity.Connectivity(load_default=True)
    
    connectivities = ['paupau','connectivity_68','connectivity_66']
    #connectivities = ['paupau']
    
    for conn_id in connectivities:
        
        conn = connectivity.Connectivity.from_file('%s.zip'%conn_id)

        tvbr = TVBReader(model, conn, id=conn_id)

        from neuroml.hdf5.NetworkBuilder import NetworkBuilder

        neuroml_handler = NetworkBuilder()

        tvbr.parse(neuroml_handler)   

        nml_file_name = '%s.net.nml'%conn_id

        from neuroml.writers import NeuroMLWriter
        NeuroMLWriter.write(neuroml_handler.get_nml_doc(),nml_file_name)