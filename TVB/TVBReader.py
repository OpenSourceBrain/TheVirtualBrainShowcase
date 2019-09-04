
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
        
        self.population_ids = []
        

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
            self.population_ids.append(pop_id)
            
            self.component = '%sDefault'%self.model.__class__.__name__.lower()
            color = '%s %s %s'%(random.random(),random.random(),random.random())
      
            properties={'color':color, 'radius':5000}
            
            self.handler.handle_population(pop_id, 
                                           self.component, 
                                           1,
                                           properties=properties)
            centre = conn.centres[ri]
            
            print('Adding population %s at %s properties %s'%(pop_id,centre,properties))
            
            self.handler.handle_location(0, 
                                         pop_id, 
                                         self.component, 
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
                if weight>111110:
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
                                         pre_pop, 
                                         post_pop, 
                                         synapse)
            

        
    
if __name__ == '__main__':

    from tvb.simulator.lab import *

    from utils import *
    from pyneuroml.lems import generate_lems_file_for_neuroml
    from pyneuroml import pynml
    
    #model = models.Kuramoto()
    model = models.JansenRit()
    #print(dir(model))
    
    conn2 = get_2_region_conn(weight_between=0)
    conn1 = get_1_region_conn()
    conn = connectivity.Connectivity(load_default=True)
    
    connectivities = ['paupau','connectivity_68','connectivity_66']
    connectivities = ['paupau', conn1]
    
    for conn_id in connectivities:
        
        if type(conn_id)==str:
            conn = connectivity.Connectivity.from_file('%s.zip'%conn_id)
        else:
            conn = conn_id
            conn_id = 'Conn%sRegion'%len(conn.region_labels)

        tvbr = TVBReader(model, conn, id=conn_id)

        from neuroml.hdf5.NetworkBuilder import NetworkBuilder

        neuroml_handler = NetworkBuilder()

        tvbr.parse(neuroml_handler)   

        nml_file_name = '../NeuroML2/%s.net.nml'%conn_id

        from neuroml.writers import NeuroMLWriter
        
        nml_doc = neuroml_handler.get_nml_doc()
        incl = neuroml.IncludeType('../TVB_LEMS/defaultModels.xml')
        nml_doc.includes.append(incl) 
        lemsfile = '../TVB_LEMS/%s.lems.xml'%model.__class__.__name__.lower()
        incl = neuroml.IncludeType(lemsfile)
        nml_doc.includes.append(incl) 
        
        NeuroMLWriter.write(nml_doc,nml_file_name)
        
        lems_ref = 'Sim_%s'%conn_id
        lems_file_name = 'LEMS_%s.xml'%lems_ref
        
        gen_plots_for_quantities = {}
        gen_saves_for_quantities = {}
        
        for pop in tvbr.population_ids:
            r = 'Vars_%s'%(pop)
            gen_plots_for_quantities[r]=[]
            for sv in model.state_variables:
                q = '%s/0/%s/%s'%(pop,tvbr.component,sv)
                gen_plots_for_quantities[r].append(q)
        
        generate_lems_file_for_neuroml(lems_ref, 
                                       nml_file_name, 
                                       conn_id, 
                                       1000, 
                                       0.1, 
                                       lems_file_name,
                                       target_dir='../NeuroML2',
                                       nml_doc=nml_doc, # Use this if the nml doc has already been loaded (to avoid delay in reload)
                                       
                                       gen_plots_for_all_v=False,
                                       plot_all_segments=False,
                                       gen_plots_for_quantities=gen_plots_for_quantities, # Dict with displays vs lists of quantity paths
                                       
                                       gen_saves_for_all_v=False,
                                       save_all_segments=False,
                                       gen_saves_for_quantities=gen_saves_for_quantities, # Dict with file names vs lists of quantity paths
                                       
                                       copy_neuroml=True,
                                       lems_file_generate_seed=12345,
                                       report_file_name='report.%s.txt' % lems_ref,
                                       simulation_seed=6789,
                                       verbose=True)