import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import time

# Gaussian gravitational constant (in AU^3 / day^2 / solar_mass)
#k = 1

k = 0.01720209895

initial_pos = np.array([])
initial_vel = np.array([])
masses = np.array([])

run_time_taken = 0

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
                accelerations[i] += k**2 * masses[j] * r_ij / distance**3
    
    # Derivative of position is velocity, derivative of velocity is acceleration
    derivatives = np.concatenate((velocities.flatten(), accelerations.flatten()))
    return derivatives    

# Initial conditions (positions in AU, velocities in AU/day)
def initial_conditions():

    global initial_pos
    global initial_vel

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

    print("Initial Positions Again:", pos_init)
    
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
