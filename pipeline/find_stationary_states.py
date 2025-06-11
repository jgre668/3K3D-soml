from sympy import *
import numpy as np

def find_stationary_states(params):
    """ Returns the upper and lower stable stationary states of the system"""

    kappa1 = params['kappa1']
    kappa3 = params['kappa3']
    kappa4 = params['kappa4']
    lamda = params['lambda']

    # asymmetry condition
    assert kappa1 > 0, "kappa_1 must be positive"
    # bistability condition
    assert -27*kappa1**2 + 4*(lamda - kappa3 - kappa4)**2 > 0, "Invalid parameters for bistability"

    k1, k3, k4, l, u = symbols("k1 k3 k4 l u")

    # set up the cubic with the parameters substituted in
    cubic = Eq((l - k3 - k4)*u - u**3 + k1,0).subs({k1 : kappa1, k3: kappa3, k4 : kappa4, l : lamda})

    # solve for stationary states
    u0_p, _, u0_n = solve(cubic, u)

    # removes small imaginary component (numerical error)
    u0_p = np.real(complex(u0_p))
    u0_n = np.real(complex(u0_n))

    return u0_p, u0_n