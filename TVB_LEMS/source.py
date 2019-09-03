"""Source of model components used to generate LEMS files (until LEMS files are considered authoritative).
"""

import numpy as np


class SVar:
    """Metadata for single state variable.
    """
    def __init__(self, name, drift, diffs, limit):
        self.name = name
        self.drift = drift
        self.diffs = diffs
        self.limit = limit


class Model:
    """Metadata for mass model.
    """
    def __init__(self, name, input, param, obsrv, const, auxex, state_space, descr=""):
        self.name = name
        self.input = input
        self.param = param
        self.obsrv = obsrv
        self.const = const
        self.auxex = auxex
        self.state_space = state_space
        self.descr = descr


test_model = Model(
    name="test",
    descr="Test model",
    input=['i1'],
    param=['a', 'b', 'c'],
    auxex=[('y1_3', 'y1 * y1 * y1')],
    obsrv=['y1'],
    const={'d': 3.0, 'e': -12.23904e-2, 'a': 1.05, 'b': 3.0, 'c': 1e-5},
    state_space=[
        SVar('y1', '(y1 - y1_3/3 + y2 + e)*b', 'c', (-1.0, 1.0)),
        SVar('y2', '(a - y1 + i1 + d)/b', 'c', (-1.0, 1.0))
    ]
)


kuramoto = Model(
    name="kuramoto",
    descr="Kuramoto model of phase synchronization.",
    state_space=[SVar('theta', 'omega + I', '0', (0, np.pi))],
    input=['I'],
    param=['omega'],
    obsrv=['sin(theta)'],
    const={'omega': 1.0},
    auxex=[],
)


g2do = Model(
    name="g2do",
    descr='Generic nonlinear 2-D (phase plane) oscillator.',
    input=['c_0'],
    param=['a'],
    obsrv=['W', 'V'],
    const={'tau': 1.0, 'I': 0.0, 'a': -2.0, 'b': -10.0, 'c': 0.0, 'd': 0.02, 'e': 3.0, 'f': 1.0, 'g': 0.0, 'alpha': 1.0, 'beta': 1.0, 'gamma': 1.0},
    state_space=[
        SVar('V', 'd * tau * (alpha*W - f*V**3 + e*V**2 + g*V + gamma*I + gamma*c_0)', 0.001, (-5, 5)),
        SVar('W', 'd * (a + b*V + c*V**2 - beta*W) / tau', 0.001, (-5, 5)),
    ],
    auxex=[]
)


jansenrit = Model(
    name="jansenrit",
    descr='Jansen-Rit model of visual evoked potentials.',
    input=['lrc'],
    param=['v0', 'r'],
    obsrv=['y0 - y1'],
    const={'A': 3.25, 'B': 22.0, 'a': 0.1, 'b': 0.05, 'v0': 5.52, 'nu_max': 0.0025, 'r': 0.56, 'J': 135.0, 'a_1': 1.0, 'a_2': 0.8, 'a_3': 0.25, 'a_4': 0.25, 'mu': 0.22},
    auxex=[('sigm_y1_y2', '2 * nu_max / (1 + exp(r * (v0 - (y1 - y2))))'), ('sigm_y0_1', '2 * nu_max / (1 + exp(r * (v0 - (a_1 * J * y0))))'), ('sigm_y0_3', '2 * nu_max / (1 + exp(r * (v0 - (a_3 * J * y0))))')],
    state_space=[
        SVar('y0', 'y3', 0, (-1, 1)),
        SVar('y1', 'y4', 0, (-500, 500)),
        SVar('y2', 'y5', 0, (-50, 50)),
        SVar('y3', 'A * a * sigm_y1_y2 - 2 * a * y3 - a**2 * y0', 0, (-6, 6)),
        SVar('y4', 'A * a * (mu + a_2 * J * sigm_y0_1 + lrc) - 2 * a * y4 - a**2 * y1', 0, (-20, 20)),
        SVar('y5', 'B * b * (a_4 * J * sigm_y0_3) - 2 * b * y5 - b**2 * y2', 0, (-500, 500)),
    ]
)


hmje = Model(
    name="hmje",
    descr='Hindmarsh-Rose-Jirsa Epileptor model of seizure dynamics.',
    input=['c1', 'c2'],
    param=['x0', 'Iext', 'r'],
    obsrv=['x1', 'x2', 'z', '-x1 + x2'],
    const={'Iext2': 0.45, 'a': 1.0, 'b': 3.0, 'slope': 0.0, 'tt': 1.0, 'c': 1.0, 'd': 5.0, 'Kvf': 0.0, 'Ks': 0.0, 'Kf': 0.0, 'aa': 6.0, 'tau': 10.0, 'x0': -1.6, 'Iext': 3.1, 'r': 0.00035},
    state_space=[
        # TODO structure if-else to generate ConditionalDerivedVariable

        # d/dt x1 = tt * (...)

        # x1_{t+1} = x1_{t} + dt * (tt * (...))

        SVar('x1', 'tt * (y1 - z + Iext + Kvf * c1 + (  (x1 <  0)*(-a * x1 * x1 + b * x1)+ (x1 >= 0)*(slope - x2 + 0.6 * (z - 4)**2)) * x1)', 0, (-2, 1)),
        SVar('y1', 'tt * (c - d * x1 * x1 - y1)', 0, (20, 2)),
        SVar('z', 'tt * (r * (4 * (x1 - x0) - z +  Ks * c1))', 0, (2, 5)),
        SVar('x2', 'tt * (-y2 + x2 - x2*x2*x2 + Iext2 + 2 * g - 0.3 * (z - 3.5) + Kf * c2)', 0.0003, (-2, 0)),
        SVar('y2', 'tt * ((-y2 + (x2 >= (-0.25)) * (aa * (x2 + 0.25))) / tau)', 0.0003, (0, 2)),
        SVar('g', 'tt * (-0.01 * (g - 0.1 * x1))', 0, (-1, 1)),
    ],
    auxex=[]
)


linear = Model(
    name="linear",
    descr='Linear differential equation',
    input=['c'],
    param=['lam'],
    obsrv=['x'],
    const={'lam': -1},
    state_space=[
        SVar('x', 'lam * x + c', 0.01, (-10, 10)),
    ],
    auxex=[]
)


rww = Model(
    name="rww",
    descr='Reduced Wong-Wang firing rate model.',
    input=['c'],
    param=['w', 'io'],
    obsrv=['S'],
    const={'a': 0.27, 'b': 0.108, 'd': 154.0, 'g': 0.641, 'ts': 100.0, 'J': 0.2609, 'w': 0.6, 'io': 0.33},
    auxex=[('x', 'w * J * S + io + J * c'), ('h', '(a * x - b) / (1 - exp(-d*(a*x - b)))')],
    state_space=[
        SVar('S', '- (S / ts) + (1 - S) * h * g', 0.01, (0, 1)),
    ]
)