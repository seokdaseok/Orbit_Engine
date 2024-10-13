from math import *
import matplotlib.pyplot as plt
import numpy as np

import time

G = 1

k = 0.01720209895

run_time_taken = 0

position_results = np.array([])

def magnitude(vector):
    return sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

##this calculates the force
def gravity(vector, relativeMass):
    top = G * relativeMass
    bottom = np.linalg.norm(vector)**2

    return -1 * (top/bottom) * (vector / np.linalg.norm(vector))

def applyAcceleration(pos, vel, deltaT, accel):

    deltaP = vel * deltaT + 0.5 * accel * deltaT**2

    deltaV = accel * deltaT

    newP = pos + deltaP
    newV = vel + deltaV

    return newP, newV

##planet data is given as a numpy array with the form [x,y,z, vx,vy,vz, mass, id]

def _simLoop(deltaT, duration, planetsList):
    start_time = time.time()

    planets_positions_list = []

    for planet in planetsList:
        planets_positions_list.append(np.array([planet[:3]]))

    for i in range(int(duration / deltaT)):

        # newPosList = []

        # newVelList = []

        ##calculates the position and velocities of the existing objects in orbit
        j = 0

        for planet in planetsList:

            accelerationSum = np.array([0.0, 0.0, 0.0])

            myId = planet[7]

            for thePlanet in planetsList:

                if thePlanet[7] != myId:

                    #print(myId)

                    ##applies an acceleration due to each individual planet based on newton's law of gravitation
                    accelerationSum += gravity(planet[:3] - thePlanet[:3], thePlanet[6])

            ##assumes constant acceleration, and changes the velocity based on the calculated acceleration
            posVelValues = applyAcceleration(planet[:3], planet[3:6], deltaT, accelerationSum)

            ##adds the new position and velocity values to the original list that stored them

            planet[:3] = posVelValues[0]
            planet[3:6] = posVelValues[1]

            planets_positions_list[j] = np.vstack([planets_positions_list[j], planet[:3]])

            j += 1

    global position_results
    position_results = planets_positions_list

    end_time = time.time()

    the_time_taken = round((end_time - start_time), 3)

    global run_time_taken
    run_time_taken = the_time_taken


        


