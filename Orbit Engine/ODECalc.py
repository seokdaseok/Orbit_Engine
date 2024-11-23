import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import time

# Gaussian gravitational constant (in AU^3 / day^2 / solar_mass)
#k = 1

k = 0.01720209895

#Universal Gravitational Constant

big_G = 6.674010551359e-11
m_sol = 1.988416e30 #kgs
day_in_secs = 86400 #seconds


initial_pos = np.array([])
initial_vel = np.array([])
masses = np.array([])

run_time_taken = 0

def find_shortest_distances():
    #shortest_distance = 1e50

    n = initial_pos.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            if i == 0 and j == 1:
                shortest_distance = np.linalg.norm(initial_pos[i] - initial_pos[j])
            else:
                distance = np.linalg.norm(initial_pos[i] - initial_pos[j])
                
                if (distance < shortest_distance):
                    shortest_distance = distance

    return shortest_distance

def find_largest_distance():
    largest_distance = 1

    n = initial_pos.shape[0]

    for i in range(n):
        for j in range(i + 1, n):
            distance = np.linalg.norm(initial_pos[i] - initial_pos[j])

            if (distance > largest_distance):
                largest_distance = distance

    return largest_distance

# Function to compute the derivatives using the Gaussian gravitational constant
def n_body_equations_gaussian(t, y, masses):
    N = len(masses)
    positions = y[:3*N].reshape((N, 3))  # Position part of the state vector
    velocities = y[3*N:].reshape((N, 3))  # Velocity part of the state vector

    #print("All Positions:", positions)
    
    accelerations = np.zeros_like(positions)
    
    # Newton's Law of Gravitation
    for i in range(N):
        for j in range(N):
            if i != j:
                r_ij = positions[j] - positions[i]
                distance = np.linalg.norm(r_ij)
                #print("Vector: ", r_ij)
                #sprint("Distance:", distance)
                normalization_factor = (1 / nu**3) * m_sol * day_in_secs**2
                accelerations[i] += big_G * masses[j] / (distance**3) * r_ij * normalization_factor

                #accelerations[i] += (k**2 / normalized_dist**3) * masses[j] * r_ij / distance**3
    
    # Derivative of position is velocity, derivative of velocity is acceleration
    derivatives = np.concatenate((velocities.flatten(), accelerations.flatten()))
    return derivatives    

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

    #positions = initial_pos
    #velocities = initial_vel

    ##OUTSIDE OF GUI TESTING

    # positions = np.array([
    #     [0, 0, 0],
    #     [1, 0, 0] 
    # ])
    
    # velocities = np.array([
    #     [0, 0, 0],  
    #     [0, 1, 0]  
    # ])
    
    return initial_pos.flatten(), initial_vel.flatten()
    #return positions.flatten(), velocities.flatten()

# Simulate N bodies using the Gaussian gravitational constant
def simulate_n_body_gaussian(t_span, rtol_val, t_eval=None):
    start_time = time.time()

    N = len(masses)
    
    # Get predefined positions and velocities
    pos_init, vel_init = initial_conditions()

    print("Normalized:", pos_init)
    
    # Combine the positions and velocities into one state vector
    y0 = np.concatenate((pos_init, vel_init))
    
    # Use solve_ivp to solve the N-body problem
    sol = solve_ivp(n_body_equations_gaussian, t_span, y0, args=(masses,), t_eval=t_eval, rtol=rtol_val)

    end_time = time.time()

    the_time_taken = round((end_time - start_time), 3)

    global run_time_taken
    run_time_taken = the_time_taken
    
    return sol

# Plotting the orbits
def plot_orbits_gaussian(sol, masses):
    N = len(masses)
    
    # Extract the positions from the solution
    positions = sol.y[:3*N].reshape((N, 3, -1))  # (N bodies, 3 dimensions, time steps)

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

##OUTSIDE OF GUI TESTING

# masses = np.array([1.0, 3.003e-6])  # Sun, Earth, Mars in solar masses
# t_span = (0, 6.34) 
# t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Time points to evaluate

# # Simulate the orbits
# sol = simulate_n_body_gaussian(t_span, 1e-8, t_eval)

# # Plot the results
# plot_orbits_gaussian(sol, masses)
