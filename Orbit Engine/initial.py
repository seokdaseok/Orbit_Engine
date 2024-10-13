import numpy as np
import matplotlib.pyplot as plt
import random


listOfPlanetsInScene = []

def string_to_list(s):
    # Split the string by commas and convert each element to a float
    return [float(x) for x in s.split(',')]

def generate_random_6_digit_number():
    return random.randint(100000, 999999)

def generate_random_3_digit_number():
    return random.randint(100, 999)

def generatePlanetFromString(pos_string, velocity_string, mass_string):

    pos_list = string_to_list(pos_string)
    vel_list = string_to_list(velocity_string)

    mass_value = float(mass_string)

    planet_data = pos_list + vel_list
    planet_data.append(mass_value)

    my_id = str(int(float(mass_string))) + "0" + str(len(listOfPlanetsInScene)) + "0" + str(generate_random_6_digit_number())

    for i in listOfPlanetsInScene:
        if my_id == i[7]:
            my_id = my_id + "0" + generate_random_3_digit_number()


    my_id_int = int(my_id)

    planet_data.append(my_id_int)

    planet_data_np = np.array(planet_data)

    listOfPlanetsInScene.append(planet_data_np)