import numpy as np
import matplotlib.pyplot as plt

import orbitCalcBasic as OCB

import velocityVerlet as vV

import initial as init

import odeTest as ode2b

_timeStep = 0.001
duration = 2.0

t_eval_step = 10000

run_time_taken = 0

planet_list_data = np.array([])

planet_position_data = np.array([])

def set_conditions(ts, dur):
    global _timeStep
    _timeStep = ts

    global duration
    duration = dur


def run_thing():
    planetsFinalList = init.listOfPlanetsInScene

    if(len(planetsFinalList) >= 1):

        #velocity verlet
        vV._simLoop(_timeStep, duration, planetsFinalList)
        global run_time_taken
        run_time_taken = vV.run_time_taken

        #OCB

        # OCB._simLoop(_timeStep, duration, planetsFinalList)
        # global run_time_taken
        # run_time_taken = OCB.run_time_taken

        ##using ode stuff
        # init_conditions = [planetsFinalList[0][0:6], planetsFinalList[1][0:6]]
        # masses = [planetsFinalList[0][6], planetsFinalList[1][6]]
        # masses = np.array(masses)

        # print(init_conditions)
        # print(masses)

        # t_span = (0, duration)

        # t_eval = np.linspace(t_span[0], t_span[1], t_eval_step)

        # ode2b.simulate(init_conditions, masses, t_span, t_eval)

def get_results():

    global planet_position_data
    planet_position_data = vV.position_results
    #planet_position_data = ode2b.planet_position_data