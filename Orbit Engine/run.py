import numpy as np
import matplotlib.pyplot as plt

import orbitCalcBasic as OCB

import velocityVerlet as vV

import ODECalc as ODE

import initial as init


_timeStep = 0.001
duration = 365

t_eval_step = round(duration / _timeStep)

_rtol = 1e-9

run_time_taken = 0

planet_list_data = np.array([])

planet_list_count = 0

planet_position_data = np.array([])
planet_velocity_data = np.array([])

largest_dist = 1

def set_conditions(ts, dur, rtol):
    global _timeStep
    _timeStep = ts

    global duration
    duration = dur

    global _rtol
    _rtol = rtol

    global t_eval_step
    t_eval_step = round(duration / _timeStep)


def run_thing():
    planetsFinalList = init.listOfPlanetsInScene

    if(len(planetsFinalList) >= 1):

        #velocity verlet

        # vV._simLoop(_timeStep, duration, planetsFinalList)
        # global run_time_taken
        # run_time_taken = vV.run_time_taken

        #OCB

        # OCB._simLoop(_timeStep, duration, planetsFinalList)
        # global run_time_taken
        # run_time_taken = OCB.run_time_taken

        #ODE

        ode_positions = []
        ode_velocities = []
        ode_masses = []

        # print("List of Planets: ", planetsFinalList, "\n")

        for planet in planetsFinalList:
            ode_positions.append(planet[:3])
            ode_velocities.append(planet[3:6])
            ode_masses.append(planet[6])

        global planet_list_count
        planet_list_count = len(ode_masses)

        ode_positions = np.array(ode_positions)
        ode_velocities = np.array(ode_velocities)
        ode_masses = np.array(ode_masses)

        print("Initial Positions: ", ode_positions)

        ODE.initial_pos = ode_positions
        ODE.initial_vel = ode_velocities
        ODE.masses = ode_masses

        global largest_dist

        largest_dist = ODE.find_largest_distance()

        ode_t_span = (0, duration)
        ode_t_eval = np.linspace(ode_t_span[0], ode_t_span[1], t_eval_step)

        solutions = ODE.simulate_n_body_gaussian(ode_t_span, _rtol, ode_t_eval)

        largest_dist *= (1.496e11/ODE.nu)

        #print(solutions)

        N = len(ode_masses)
        # print(N)
        #print("Solutions Shape: ", solutions.y.shape)
        # print("\n")
        # print("Solutions: ", solutions.y, "\n")

        #shape of the solutions are: planet 1: x,y,z,vx,vy,vz, planet 2: x,y,z,vx,vy,vz

        global planet_position_data

        global planet_velocity_data

        #num_planets = solutions.y.shape[0] // 6
        timesteps = solutions.y.shape[1]

        print("Solutions.Y:", solutions.y[:3*N])
        print("Solutions Shape: ", solutions.y[:3*N].shape)

        positions_a = solutions.y[:3*N].reshape((N, 3, -1))

        velocities_a = solutions.y[3*N:].reshape((N, 3, -1))

        # data_reshape = solutions.y.reshape(N, 3, timesteps)

        # positions = data_reshape[:, :3, :]

        #planet_position_data = positions.transpose(0, 2, 1)
        planet_position_data = positions_a
        planet_velocity_data = velocities_a

        # print(planet_position_data)

        # print("\n")

        global run_time_taken
        run_time_taken = ODE.run_time_taken


def get_results():
    global planet_position_data
    #planet_position_data = vV.position_results
    #planet_position_data = ode2b.planet_position_data
