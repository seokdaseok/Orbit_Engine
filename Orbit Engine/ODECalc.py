import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import time

# Gaussian gravitational constant (in AU^3 / day^2 / solar_mass)
#k = 1

#gaussian gravitational constant (not used)
k = 0.01720209895

#Constants for unit conversion

big_G = 6.674010551359e-11
m_sol = 1.988416e30 #kgs
day_in_secs = 86400 #seconds

#creates numpy arrays for the initial conditions which will be changed with run.py
initial_pos = np.array([])
initial_vel = np.array([])
masses = np.array([])

#sets the run time as 0
run_time_taken = 0

def find_shortest_distances():

    n = initial_pos.shape[0]


    #loops through every combination of distances out of the iniital conditions to find the shortest distance

    for i in range(n):
        for j in range(i + 1, n):
            if i == 0 and j == 1: # if this is the first combination, the shortest distance is set to be that distance
                shortest_distance = np.linalg.norm(initial_pos[i] - initial_pos[j]) # takes the magnitude of the distance
            else:
                distance = np.linalg.norm(initial_pos[i] - initial_pos[j]) # finds the distance between 2 planets
                
                if (distance < shortest_distance): # if the distance is smaller than the previous shortest distance, the new shortest distance is the current distance
                    shortest_distance = distance

    return shortest_distance # returns the value of the shortest distance

#same function as the shortest distance function, but finds the largest distance instead

def find_largest_distance():
    largest_distance = 1

    n = initial_pos.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            distance = np.linalg.norm(initial_pos[i] - initial_pos[j])

            if (distance > largest_distance):
                largest_distance = distance

    return largest_distance

# Function to compute the derivatives according to Newton's Law of Gravitation
def n_body_equations_gaussian(t, y, masses):

    N = len(masses)

    # reshapes position and velocity vectors from a 3 dimensional array, into a 2 dimensional array where every 6 values is a new planet.
    # this is the format that the ODE solver accepts

    positions = y[:3*N].reshape((N, 3))  # Position part of the state vector
    velocities = y[3*N:].reshape((N, 3))  # Velocity part of the state vector
    
    accelerations = np.zeros_like(positions) #generates a list of accelerations (which all start as 0)

    normalization_factor = (1 / nu**3) * m_sol * day_in_secs**2 # creates the normalization factor
    
    # Newton's Law of Gravitation

    for i in range(N): # loops for every planet
        for j in range(N): # every planet must interact with every other planet, so there is another loop
            if i != j: # to not compute the gravity with itself

                r_ij = positions[j] - positions[i] # finds the displacement vector between the 2 planets

                distance = np.linalg.norm(r_ij) # computes the magnitude
 
                accelerations[i] += big_G * masses[j] / (distance**3) * r_ij * normalization_factor # finds the sun of the acceleration due to every other planet onto the planet with index i

    
    # Derivative of position is velocity, derivative of velocity is acceleration
    derivatives = np.concatenate((velocities.flatten(), accelerations.flatten()))

    return derivatives # returns the derivatives for ODE code to work

# Initial conditions (positions in AU, velocities in AU/day)

def initial_conditions():

    global initial_pos
    global initial_vel

    #convert from AU to meters

    initial_pos = initial_pos * 1.496e11

    #convert from AU/Day to meters / day

    initial_vel = initial_vel * 1.496e+11

    ##normalization code
    global nu
    nu = find_shortest_distances()

    initial_pos = initial_pos / nu

    initial_vel = initial_vel / nu

    return initial_pos.flatten(), initial_vel.flatten()
    #return positions.flatten(), velocities.flatten()

# Simulate N bodies using the Gaussian gravitational constant
def simulate_n_body_gaussian(t_span, rtol_val, t_eval=None):
    start_time = time.time()

    N = len(masses)
    
    # Get predefined positions and velocities
    pos_init, vel_init = initial_conditions()
    
    # Combine the positions and velocities into one state vector
    y0 = np.concatenate((pos_init, vel_init))
    
    # Use solve_ivp to solve the N-body problem
    sol = solve_ivp(n_body_equations_gaussian, t_span, y0, args=(masses,), t_eval=t_eval, rtol=rtol_val)

    end_time = time.time()

    the_time_taken = round((end_time - start_time), 3)

    global run_time_taken
    run_time_taken = the_time_taken
    
    return sol

## NOT USED IN GUI, ONLY USED FOR TESTING OUTSIDE OF IT ##

def plot_orbits(sol, masses):
    N = len(masses)
    
    # Extract the positions from the solution
    positions = sol.y[:3*N].reshape((N, 6, -1))  # (N bodies, 3 dimensions, time steps)

    print(positions)
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    for i in range(N):
        ax.plot(positions[i, 0], positions[i, 1], positions[i, 2], label=f'Body {i+1}')
    
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.legend()
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    plt.show()

# masses = np.array([1.0, 3.003e-6])  # Sun, Earth, Mars in solar masses
# t_span = (0, 6.34) 
# t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Time points to evaluate

# # Simulate the orbits
# sol = simulate_n_body_gaussian(t_span, 1e-8, t_eval)

# # Plot the results
# plot_orbits(sol, masses)
