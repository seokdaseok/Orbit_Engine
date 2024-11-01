import numpy as np
import matplotlib.pyplot as plt

import orbitCalcBasic as OCB

import velocityVerlet as vV

import ODECalc as ODE

import initial as init


_timeStep = 0.001
duration = 6.34

t_eval_step = round(duration / _timeStep)

run_time_taken = 0

_rtol = 1e-9

planet_list_data = np.array([])

planet_position_data = np.array([])

def set_conditions(ts, dur, rtol):
    global _timeStep
    _timeStep = ts

    global duration
    duration = dur

    global _rtol
    _rtol = rtol


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

        print("List of Planets: ", planetsFinalList, "\n")

        for planet in planetsFinalList:
            ode_positions.append(planet[:3])
            ode_velocities.append(planet[3:6])
            ode_masses.append(planet[6])

        ode_positions = np.array(ode_positions)
        ode_velocities = np.array(ode_velocities)
        ode_masses = np.array(ode_masses)

        ODE.initial_pos = ode_positions
        ODE.initial_vel = ode_velocities
        ODE.masses = ode_masses

        ode_t_span = (0, duration)
        ode_t_eval = np.linspace(ode_t_span[0], ode_t_span[1], t_eval_step)

        solutions = ODE.simulate_n_body_gaussian(ode_t_span, _rtol, ode_t_eval)

        #print(solutions)

        N = len(ode_masses)
        print("Solutions Shape: ", solutions.y.shape)
        print("Solutions: ", solutions.y, "\n")

        global planet_position_data
        planet_position_data = solutions.y[:3*N].reshape((N, 3, -1))

        print("Position Data: ", planet_position_data, "\n")

        global run_time_taken
        run_time_taken = ODE.run_time_taken


def get_results():

    global planet_position_data
    #planet_position_data = vV.position_results
    #planet_position_data = ode2b.planet_position_data
