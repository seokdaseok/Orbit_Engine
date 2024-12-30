import numpy as np
import matplotlib.pyplot as plt

import orbitCalcBasic as OCB

import velocityVerlet as vV

import ODECalc as ODE

import initial as init

# variables to store the values used by the simulation

_timeStep = 0.0001

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

        #Basic Orbit Calculation Code

        # OCB._simLoop(_timeStep, duration, planetsFinalList)
        # global run_time_taken
        # run_time_taken = OCB.run_time_taken

        #ODE Method

        # creates list to store the initial conditions for the ODE

        ode_positions = []
        ode_velocities = []
        ode_masses = []

        # takes the values from the list of planets in initial.py and saves them into these lists

        for planet in planetsFinalList:
            ode_positions.append(planet[:3])
            ode_velocities.append(planet[3:6])
            ode_masses.append(planet[6])

        # saves a count for the number of planets in the simulation (equal to the number of masses)

        global planet_list_count
        planet_list_count = len(ode_masses)

        # turns everything into a numpy array

        ode_positions = np.array(ode_positions)
        ode_velocities = np.array(ode_velocities)
        ode_masses = np.array(ode_masses)

        # sets the arrays in the ODE code to equal the arrays from this script

        ODE.initial_pos = ode_positions
        ODE.initial_vel = ode_velocities
        ODE.masses = ode_masses

        # Finds the largest distance

        global largest_dist

        largest_dist = ODE.find_largest_distance()

        # Setting up the ODE
        ode_t_span = (0, duration)

        # creating a linspace for the ODE code to use
        ode_t_eval = np.linspace(ode_t_span[0], ode_t_span[1], t_eval_step)

        #uses the simulation function to generate the list of positions
        solutions = ODE.simulate_n_body_gaussian(ode_t_span, _rtol, ode_t_eval)

        #turns the largest_dist to be in terms of the normalized scale factor
        largest_dist *= (1.496e11/ODE.nu)

        N = len(ode_masses)

        global planet_position_data

        global planet_velocity_data

        #reshapes the solutions to a Nx3xM array (M for each individual planet, 3 for x,y,z, and M for all the values)

        planet_position_data = solutions.y[:3*N].reshape((N, 3, -1))

        planet_velocity_data = solutions.y[3*N:].reshape((N, 3, -1))

        #saves the run time
        global run_time_taken
        run_time_taken = ODE.run_time_taken


def get_results():
    global planet_position_data
