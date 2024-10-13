import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

G = 1

def gravitational_force(m1, m2, r):
    return ((G * m1 * m2) / (np.linalg.norm(r)**3)) * r