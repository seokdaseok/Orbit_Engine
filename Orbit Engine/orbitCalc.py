import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Constants
GM = 1  # Gravitational constant * Mass of central body

# Body class to represent each celestial body
class Body:
    def __init__(self, mass, position, velocity):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

    def gravitational_force(self, other):
        r_vec = other.position - self.position
        r_mag = np.linalg.norm(r_vec)
        force_mag = GM * self.mass * other.mass / r_mag**3
        return force_mag * r_vec

# Function to calculate the derivatives for the ODE solver
def compute_derivatives(t, state, bodies):
    num_bodies = len(bodies)
    derivatives = np.zeros_like(state)

    # Extract positions and velocities from state
    positions = state[:2*num_bodies].reshape(num_bodies, 2)
    velocities = state[2*num_bodies:].reshape(num_bodies, 2)

    # Calculate derivatives
    for i, body in enumerate(bodies):
        body.position = positions[i]
        body.velocity = velocities[i]

        # Update velocity derivatives (dx/dt = vx, dy/dt = vy)
        derivatives[2*i:2*(i+1)] = body.velocity

        # Acceleration due to gravitational force from all other bodies
        acc = np.zeros(2)
        for j, other_body in enumerate(bodies):
            if i != j:
                acc += body.gravitational_force(other_body) / body.mass

        # Update acceleration derivatives
        derivatives[2*num_bodies + 2*i:2*num_bodies + 2*(i+1)] = acc

    return derivatives

# Initializing the system with a few bodies
bodies = [
    Body(1.0, [-1, 0], [0, -0.5]),  # Body 1
    Body(1.0, [1, 0], [0, 0.5]),    # Body 2
    Body(1.0, [0, 1], [-0.5, 0])    # Body 3
]

# Flatten the initial conditions (positions and velocities)
initial_conditions = np.hstack([np.hstack([body.position for body in bodies]),
                                np.hstack([body.velocity for body in bodies])])

# Time span and points for evaluation
t_span = (0, 100)
t_eval = np.linspace(*t_span, 1000)

# Solve the system of ODEs using solve_ivp
sol = solve_ivp(compute_derivatives, t_span, initial_conditions, t_eval=t_eval, args=(bodies,))

# Extract the positions from the solution
num_bodies = len(bodies)
positions = sol.y[:2*num_bodies].reshape(num_bodies, 2, -1)

# Plot the orbits
plt.figure(figsize=(8, 8))
for i in range(num_bodies):
    plt.plot(positions[i, 0], positions[i, 1], label=f'Body {i+1}')

plt.title('Multibody Orbital Simulation')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.axis('equal')
plt.show()
