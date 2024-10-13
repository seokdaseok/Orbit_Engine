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

def applyAcceleration1(pos, vel, deltaT, accel):

    deltaP = vel * deltaT + 0.5 * accel * deltaT**2

    newP = pos + deltaP

    return newP

def applyAcceleration2(vel, deltaT, accel1, accel2):

    deltaV = 0.5 * (accel1 + accel2) * deltaT

    newV = vel + deltaV

    return newV

##planet data is given as a numpy array with the form [x,y,z, vx,vy,vz, mass, id]

def _simLoop(deltaT, duration, planetsList):
    start_time = time.time()

    planets_positions_list = []

    for planet in planetsList:
        planets_positions_list.append(np.array([planet[:3]]))

    for i in range(int(duration / deltaT)):
        
        j = 0

        ##first round of acceleration

        temporaryPositionsList = np.array([0.0,0.0,0.0])

        firstAccelerationsList = np.array([0.0,0.0,0.0])

        for planet in planetsList:

            accelerationSum = np.array([0.0, 0.0, 0.0])

            myId = planet[7]

            for thePlanet in planetsList:

                if thePlanet[7] != myId:

                    accelerationSum += gravity(planet[:3] - thePlanet[:3], thePlanet[6])


            p1 = applyAcceleration1(planet[:3], planet[3:6], deltaT, accelerationSum)

            firstAccelerationsList = np.vstack([firstAccelerationsList, accelerationSum])

            temporaryPositionsList = np.vstack([temporaryPositionsList, p1])

        ##second round of acceleration
        
        for planet in planetsList:

            accelerationSum = np.array([0.0, 0.0, 0.0])

            myId = planet[7]

            k = 0

            for thePlanet in planetsList:

                if k != j:

                    accelerationSum += gravity(temporaryPositionsList[j+1] - temporaryPositionsList[k+1], thePlanet[6])

            a1 = firstAccelerationsList[j + 1]

            p = temporaryPositionsList[j + 1]

            v = applyAcceleration2(planet[3:6], deltaT, a1, accelerationSum)

            planet[:3] = p
            planet[3:6] = v

            planets_positions_list[j] = np.vstack([planets_positions_list[j], planet[:3]])

            j += 1

    global position_results
    position_results = planets_positions_list

    end_time = time.time()

    the_time_taken = round((end_time - start_time), 3)

    global run_time_taken
    run_time_taken = the_time_taken


        


