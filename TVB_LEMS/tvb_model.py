"""TVB model from LEMS file.
"""

import os
import tvb.basic.traits.core as core
from tvb.simulator.models.base import Model as BaseModel
import lems.api as lems


def read_lems_file(fname):
    """Import LEMS model from file fname or builtin model name.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    builtin_fname = os.path.join(here, fname + '.lems.xml')
    if os.path.exists(builtin_fname):
        fname = builtin_fname
    model = lems.Model()
    model.import_from_file(fname)
    return model


class LEMSModel(core.Type):
    """Traits that wraps a LEMS model.
    """
    wraps = lems.Model


_model_template = """
class LEMS{name}Model(BaseModel):
    _ui_name = "{name_title}"
{parameters}

    state_variable_range = {state_variable_range}
    
    variables_of_interest = {variables_of_interest}
    
    state_variables = {state_variables}
    _nvar = {nvar}
    cvar = numpy.array({cvar}, dtype=numpy.uint32)
    
{dfun}
"""

_parameter_template = """
    {name} = arrays.FloatArray(
        label="{name}",
        default=numpy.array([{default}]),
        # TODO range
        # TODO doc
        order={order})
"""

_dfun_template = """
    def dfun(self, y, c, local_coupling=0.0):
        dy = np.zeros_like(y)
        # TODO
        return dy
"""

class Model(BaseModel):
    """Model built from a LEMS file.
    """

    def _build_from_lems(self, model):
        m = model  # type: lems.Model
        assert m is not None
        # TODO maybe generate all types into single file?
        ct, = m.component_types.values()  # type: lems.ComponentType
        for par in ct.parameters:
            par = par  # type: lems.Parameter
            print par

    @classmethod
    def from_lems(cls, name):
        obj = cls()
        obj._build_from_lems(read_lems_file(name))
        return obj


def model_from_lems(name):
    lems = read_lems_file(name)
    lems_ct, = lems.component_types.values()  # type: lems.ComponentType
    for param in lems_ct.parameters:
        print param
    for svar in lems_ct.dynamics.state_variables:
        print svar.name
    for ddt in lems_ct.dynamics.time_derivatives:
        print ddt.variable, ddt.expression_tree
    return lems_ct


if __name__ == '__main__':
    model_from_lems('rww')


