import numpy as np
from scipy.optimize import curve_fit

def linear(x, a, b):
    """
    Linear function compatible with scipy.optimize.curve_fit.
    """
    return a*x+b

def quadratic(x, a, b, c):
    """
    Quadratic function compatible with scipy.optimize.curve_fit.
    """
        return a*x**2+b*x+c