import numpy as np

file_name = "planet_data.csv"

def create_planet_csv(planetList, directory):
    planetList = np.array(planetList)

    np.savetxt(directory, planetList, delimiter=",")


def pull_planets(directory):
    data = np.loadtxt(directory, delimiter=',')

    return data


