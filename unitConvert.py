import numpy as np

def convert_velocity_to_AU_per_Day(vector):
    value = 365.2568983 / (2 * np.pi)
    return vector / value

