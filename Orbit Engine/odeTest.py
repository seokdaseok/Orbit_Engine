import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

planet_position_data = []

# Gaussian gravitational constant (AU^3/day^2/M_sun)
G = 1

def gravitational_force(m1, m2, r):
    return ((G * m1 * m2) / (np.linalg.norm(r)**3)) * r

def equations_of_motion(t, y, masses):
    r1 = y[0:3]  # Position of planet 1
    v1 = y[3:6]  # Velocity of planet 1
    r2 = y[6:9]  # Position of planet 2
    v2 = y[9:12] # Velocity of planet 2

    r12 = r2 - r1  # Vector from planet 1 to planet 2

    # Calculate forces
    F12 = gravitational_force(masses[0], masses[1], r12)  # Force on planet 1 due to planet 2

    # Accelerations
    a1 = F12 / masses[0]
    a2 = -F12 / masses[1]

    return np.concatenate([v1, a1, v2, a2])

def simulate_orbits(initial_conditions, masses, t_span, t_eval):
    # Flatten the initial conditions to a single array
    y0 = np.concatenate(initial_conditions)

    # Integrate the ODEs
    solution = solve_ivp(equations_of_motion, t_span, y0, args=(masses,), t_eval=t_eval, rtol=1e-9, atol=1e-9)

    return solution

def plot_orbits(solution):
    r1 = solution.y[0:3, :]
    r2 = solution.y[6:9, :]
    
    plt.figure(figsize=(10, 10))
    plt.plot(r1[0], r1[1], label="Planet 1")
    plt.plot(r2[0], r2[1], label="Planet 2")
    plt.xlabel('x (AU)')
    plt.ylabel('y (AU)')
    plt.xlim([-1.5, 1.5])
    plt.ylim([-1.5, 1.5])
    plt.title('Orbital Paths of Two Planets')
    plt.legend()
    plt.grid()
    plt.show()

# Initial conditions: [x, y, z, vx, vy, vz] for each planet
initial_conditions = [
    np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),  # Planet 1
    np.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0]) # Planet 2
]

# Masses of the planets (in solar masses)
masses = np.array([1.0, 3e-6])

# Time span for the simulation (in days)
t_span = (0, 20)  # 10 years
t_eval = np.linspace(t_span[0], t_span[1], 1000)

#print(initial_conditions)
#print(masses)

# Run the simulation
#solution = simulate_orbits(initial_conditions, masses, t_span, t_eval)

def simulate(initial_conditions_, masses_, t_span_, t_eval_):
    print(initial_conditions_)
    print(masses_)
    solution = simulate_orbits(initial_conditions_, masses_, t_span_, t_eval_)

    r1 = solution.y[0:3, :]
    r2 = solution.y[6:9, :]

    p1 = np.transpose(r1)
    p2 = np.transpose(r2)

    planet_position_data.append(p1)
    planet_position_data.append(p2)

#simulate([np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),np.array([1.0, 0.0, 0.0, 0.0, 1.0, 0.0])], masses, t_span, t_eval)

#print(planet_position_data[1])

    
#print(solution)

# Plot the orbits
#plot_orbits(solution)
