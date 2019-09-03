"""Generate LEMS from a source.Model instance. Disparities include

- model may specify diffusion coefficients for SDE. LEMS?
- LEMS expects units, TVB doesn't.
- TVB has other metadata like docstrings on parameter values?

"""

import lems.api as lems
import source


def model_instances():
    for key in dir(source):
        member = getattr(source, key)
        if isinstance(member, source.Model):
            yield member


def build_lems_for_model(src):
    model = lems.Model()

    model.add(lems.Dimension('time', t=1))
    # model.add(lems.Dimension('au'))

    # primary element of the model is a mass model component
    mass = lems.ComponentType(src.name, extends="baseCellMembPot")
    model.add(mass)
    
    ######### Adding v is required to ease mapping to NEURON...
    mass.dynamics.add(lems.StateVariable(name="v", dimension="voltage", exposure="v"))
    
    mass.add(lems.Attachments(name="synapses",type_="basePointCurrentDL"))
    

    for input in src.input:
        mass.dynamics.add(lems.DerivedVariable(name=input, 
                                               dimension='none',
                                               exposure=input,
                                               select='synapses[*]/I',
                                               reduce='add'))
        mass.add(lems.Exposure(input, 'none'))
        
        
    for key, val in src.const.items():
        mass.add(lems.Parameter(key, 'none'))  # TODO units
        
    
        
    mass.add(lems.Constant(name="MSEC", dimension="time", value="1ms"))
    mass.add(lems.Constant(name="PI", dimension="none", value="3.14159265359"))

    states = []
    der_vars = []
    # for key in src.param:
    #     mass.add(lems.Parameter(key, 'au'))  # TODO units

    for key, val in src.auxex:
        val = val.replace('**', '^')
        mass.dynamics.add(lems.DerivedVariable(key, value=val))

    for key in src.obsrv:
        name_dv = key.replace('(','_').replace(')','').replace(' - ','_min_')
        mass.dynamics.add(lems.DerivedVariable(name_dv, value=key, exposure=name_dv))
        mass.add(lems.Exposure(name_dv, 'none'))

    for src_svar in src.state_space:
        name = src_svar.name
        ddt = src_svar.drift.replace('**', '^')
        mass.dynamics.add(lems.StateVariable(name, 'none', name))
        mass.dynamics.add(lems.TimeDerivative(name, '(%s)/MSEC'%ddt))
        mass.add(lems.Exposure(name, 'none'))
        
    ''' On condition is not need on the model but NeuroML requires its definition -->
            <OnCondition test="r .lt. 0">
                <EventOut port="spike"/>
            </OnCondition>'''
            
    oc = lems.OnCondition(test='v .gt. 0')
    oc.actions.append(lems.EventOut(port='spike'))
    mass.dynamics.add(oc)

    return model



if __name__ == '__main__':
    import os
    from lems.base.util import validate_lems
    here = os.path.dirname(os.path.abspath(__file__))
    for model in model_instances():
        fname = os.path.join(here, model.name + '.lems.xml')
        try:
            build_lems_for_model(model).export_to_file(fname)
            print('Successfully built %s'%fname)
            validate_lems(fname)
        except Exception as exc:
            print('> Error converting %s: %s'%(fname,exc))
