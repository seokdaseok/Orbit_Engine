import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Gaussian gravitational constant (AU^3/day^2/M_sun)
G = 1

k = 0.01720209895

def gravitational_acceleration(m, r):
    return -((G * m) / (np.linalg.norm(r)**3)) * r

def equations_of_motion_twobody(t, y, masses):
    r1 = y[0:3]  # Position of planet 1
    v1 = y[3:6]  # Velocity of planet 1
    r2 = y[6:9]  # Position of planet 2
    v2 = y[9:12] # Velocity of planet 2

    r12 = r2 - r1  # Vector from planet 1 to planet 2

    # Calculate forces
    F12 = gravitational_acceleration(masses[1], r12)  # Force on planet 1 due to planet 2

    # Accelerations
    a1 = F12 / masses[0]
    a2 = -F12 / masses[1]

    return np.concatenate([v1, a1, v2, a2])


def equations_of_motion(t, planetList):

    states_array = np.array([])

    num_of_planets = int(planetList.size / 8)

    for i in range(num_of_planets):

        i_planet = 8*(i)

        #i is the current planet
        p0 = planetList[i_planet:i_planet+3]
        v0 = planetList[i_planet+3:i_planet+6]

        my_conditions_array = np.array([])

        accel_sum = np.array([0.0, 0.0, 0.0])

        for j in range(num_of_planets):
            #j is the other planets

            j_planet = 8*(j)

            if (planetList[i_planet+7] != planetList[j_planet+7]):

                p_planet = planetList[j_planet:j_planet+3]

                r = p0 - p_planet
                
                accel = gravitational_acceleration(planetList[j_planet+6], r)

                accel_sum += accel

        
        my_conditions_array = np.concatenate([v0, accel_sum])

        states_array = np.concatenate([states_array, my_conditions_array, [planetList[i_planet+6], planetList[i_planet+7]]])

        
    #print(states_array)

    return states_array


def simulate_orbits(initial_conditions, t_span, t_eval):
    # Flatten the initial conditions to a single array
    y0 = np.concatenate(initial_conditions)

    # Integrate the ODEs
    solution = solve_ivp(equations_of_motion, t_span, y0, t_eval=t_eval, rtol=1e-6, atol=1e-6)

    return solution

initial_conditions = [
    np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 100]),  # Planet 1
    np.array([1.0, 0.0, 0.0, 0.0, 0.5, 0.0, 3e-6, 200]) # Planet 2
]

t_span = (0, 200)  # 10 years
t_eval = np.linspace(t_span[0], t_span[1], 1000)

solution = simulate_orbits(initial_conditions, t_span, t_eval)

print("done")

print(solution)

