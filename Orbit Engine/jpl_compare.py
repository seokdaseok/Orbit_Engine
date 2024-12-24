import numpy as np
import matplotlib.pyplot as plt


jpl_ephemeris = "S:\Orbit_Engine_Data/"

def loadJPLData(fileName):

    filePath = jpl_ephemeris + fileName

    data = np.loadtxt(filePath, delimiter=",", dtype=str)

    # julian day, x, y, z

    positionData = data[:, 2:5].astype(float)

    return positionData

def loadOrbitData(fileName):

    data = np.data = np.loadtxt(fileName, delimiter=",", dtype=str)

    positionData = data[:,0:3].astype(float)

    return positionData

#times should match up in saved data, because the orbit engine saves it by day, and so does the jpl horizons data.

def compare_positions(pos1, pos2):

    min_size = min(len(pos1), len(pos2))

    mag1 = np.linalg.norm(pos1, axis=1)[:min_size]
    mag2 = np.linalg.norm(pos2, axis=1)[:min_size]



    #print(mag1)
    #print(mag2)

    percent_error = np.abs((mag1 - mag2) / mag1) * 100

    return percent_error

def compare_specific_positions(pos1, pos2):

    min_size = min(len(pos1), len(pos2))

    pos1 = pos1[:min_size]
    pos2 = pos2[:min_size]

    x_error = np.abs((pos1[:,0] - pos2[:, 0]) / pos1[:, 0]) * 100
    y_error = np.abs((pos1[:,1] - pos2[:, 1]) / pos1[:, 1]) * 100
    z_error = np.abs((pos1[:,2] - pos2[:, 2]) / pos1[:, 2]) * 100

    return x_error, y_error, z_error

def plot_error(error_array, plot_title, color):

    plt.figure()
    plt.plot(error_array, color, label="Percent Error")
    plt.xlabel("Time")
    plt.ylabel("Error (%)")
    plt.title(plot_title)

    plt.legend()


# RUNNING EVERYTHING

def saturn_test():

    # Saturn Test #1:

    jpl_saturn = loadJPLData("saturn_jpl.txt")
    generated_saturn = loadOrbitData("sun_saturn_jupiter_data_0.000285716656_M_sun.csv")

    saturn_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data, "Saturn Error against JPL: 0.0001 Time Step, 365 Days, 1e-9 rtol", "r-")

    # Saturn Test #2 (reduced timestep):

    jpl_saturn = loadJPLData("saturn_jpl.txt")
    generated_saturn = loadOrbitData("sun_saturn_jupiter_0_00001_timestep_0.000285716656_M_sun.csv")

    saturn_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data, "Saturn Error against JPL: 0.00001 Time Step, 365 Days, 1e-9 rtol", "b-")

    # Saturn Test #3 (reduced rtol):

    jpl_saturn = loadJPLData("saturn_jpl.txt")
    generated_saturn = loadOrbitData("sun_saturn_jupiter_1e_neg11_rtol_0.000285716656_M_sun.csv")

    saturn_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data, "Saturn Error against JPL: 0.0001 Time Step, 365 Days, 1e-11 rtol", "g-")
    
    plt.show()

#saturn_test()


def long_term_test():

    ## 2014-12-20 to 2024-12-20

    #Saturn for 10 years

    jpl_saturn = loadJPLData("saturn_10yrs_jpl.txt")
    generated_saturn = loadOrbitData("sun_saturn_jupiter_10yrs_0.000285716656_M_sun.csv")

    saturn_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data, "Saturn Error against JPL: 0.0001 Time Step, 3650 Days, 1e-9 rtol", "r-")

    #Jupiter for 10 years

    jpl_jupiter = loadJPLData("jupiter_10yrs_jpl.txt")
    generated_saturn = loadOrbitData("sun_saturn_jupiter_10yrs_0.000954588_M_sun.csv")

    jupiter_error_data = compare_positions(jpl_jupiter, generated_saturn)

    plot_error(jupiter_error_data, "Jupiter Error against JPL: 0.0001 Time Step, 3650 Days, 1e-9 rtol", "b-")


    #plt.show()

#long_term_test()


def solar_system_test():

    #1 year long saturn test

    jpl_saturn = loadJPLData("saturn_10yrs_jpl.txt")
    generated_saturn = loadOrbitData("solar_system_data_0.000285716656_M_sun.csv")

    saturn_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data, "Saturn Error against JPL whole solar system: 0.0001 Time Step, 365 Days, 1e-9 rtol", "r-")

    #10 year long saturn test

    jpl_saturn = loadJPLData("saturn_10yrs_jpl.txt")
    generated_saturn = loadOrbitData("solar_system_data_10yrs_0.000285716656_M_sun.csv")

    saturn_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data, "Saturn Error against JPL whole solar system: 0.0001 Time Step, 3650 Days, 1e-9 rtol", "r-")


    plt.show()

#solar_system_test()


def individual_coordinates_test_saturn():

    ##Saturn Test

    jpl_saturn = loadJPLData("saturn_10yrs_jpl.txt")
    generated_saturn = loadOrbitData("solar_system_data_0.000285716656_M_sun.csv")

    saturn_error_data = compare_specific_positions(jpl_saturn, generated_saturn)

    saturn_overall_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data[0], "X Position Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 365 Days, 1e-9 rtol", "r-")

    plot_error(saturn_error_data[1], "Y Position Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 365 Days, 1e-9 rtol", "b-")

    plot_error(saturn_error_data[2], "Z Position Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 365 Days, 1e-9 rtol", "g-")

    plot_error(saturn_overall_error_data, "Position Magnitude Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 365 Days, 1e-9 rtol", "m-")

    plt.show()

#individual_coordinates_test_saturn()

def individual_coordinates_test_jupiter():
    jpl_jupiter = loadJPLData("jupiter_10yrs_jpl.txt")
    generated_jupiter = loadOrbitData("solar_system_data_0.000955_M_sun.csv")

    jupiter_error_data = compare_specific_positions(jpl_jupiter, generated_jupiter)

    jupiter_overall_error_data = compare_positions(jpl_jupiter, generated_jupiter)

    plot_error(jupiter_error_data[0], "X Position Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 365 Days, 1e-9 rtol", "r-")

    plot_error(jupiter_error_data[1], "Y Position Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 365 Days, 1e-9 rtol", "b-")

    plot_error(jupiter_error_data[2], "Z Position Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 365 Days, 1e-9 rtol", "g-")

    plot_error(jupiter_overall_error_data, "Position Magnitude Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 365 Days, 1e-9 rtol", "m-")

    plt.show()

#individual_coordinates_test_jupiter()

def coordinates_test_long():

    ##Jupiter

    jpl_jupiter = loadJPLData("jupiter_10yrs_jpl.txt")
    generated_jupiter = loadOrbitData("solar_system_data_10yrs_0.000955_M_sun.csv")

    jupiter_error_data = compare_specific_positions(jpl_jupiter, generated_jupiter)

    jupiter_overall_error_data = compare_positions(jpl_jupiter, generated_jupiter)

    plot_error(jupiter_error_data[0], "X Position Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "r-")

    plot_error(jupiter_error_data[1], "Y Position Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "b-")

    plot_error(jupiter_error_data[2], "Z Position Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "g-")

    plot_error(jupiter_overall_error_data, "Position Magnitude Error against JPL with whole solar system (Jupiter): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "m-")

    ##Saturn

    jpl_saturn = loadJPLData("saturn_10yrs_jpl.txt")
    generated_saturn = loadOrbitData("solar_system_data_10yrs_0.000285716656_M_sun.csv")

    saturn_error_data = compare_specific_positions(jpl_saturn, generated_saturn)

    saturn_overall_error_data = compare_positions(jpl_saturn, generated_saturn)

    plot_error(saturn_error_data[0], "X Position Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "r-")

    plot_error(saturn_error_data[1], "Y Position Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "b-")

    plot_error(saturn_error_data[2], "Z Position Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "g-")

    plot_error(saturn_overall_error_data, "Position Magnitude Error against JPL with whole solar system (Saturn): 0.0001 Time Step, 3650 Days, 1e-9 rtol", "m-")

    plt.show()

#coordinates_test_long()

def asteroid_2002_kl6_test():

    jpl_2002_kl6 = loadJPLData("2002_kl6_jpl.txt")
    generated_2002_kl6 = loadOrbitData("2002kl6_data_0.0_M_sun.csv")
    
    error_data = compare_specific_positions(jpl_2002_kl6, generated_2002_kl6)

    overall_error_data = compare_positions(jpl_2002_kl6, generated_2002_kl6)

    plot_error(error_data[0], "X Position Error against JPL for 2002 KL6: 0.0001 Time Step, 3650 Days, 1e-9 rtol", "r-")

    plot_error(error_data[1], "Y Position Error against JPL for 2002 KL6: 0.0001 Time Step, 3650 Days, 1e-9 rtol", "b-")

    plot_error(error_data[2], "Z Position Error against JPL for 2002 KL6: 0.0001 Time Step, 3650 Days, 1e-9 rtol", "g-")

    plot_error(overall_error_data, "Position Magnitude Error against JPL for 2002 KL6: 0.0001 Time Step, 3650 Days, 1e-9 rtol", "m-")

    plt.show()


def asteroid_2002_kl6_test_1yr():

    jpl_2002_kl6 = loadJPLData("2002_kl6_jpl.txt")
    generated_2002_kl6 = loadOrbitData("2002kl6_data_1yr_0.0_M_sun.csv")
    
    error_data = compare_specific_positions(jpl_2002_kl6, generated_2002_kl6)

    overall_error_data = compare_positions(jpl_2002_kl6, generated_2002_kl6)

    plot_error(error_data[0], "X Position Error against JPL for 2002 KL6: 0.0001 Time Step, 365 Days, 1e-9 rtol", "r-")

    plot_error(error_data[1], "Y Position Error against JPL for 2002 KL6: 0.0001 Time Step, 365 Days, 1e-9 rtol", "b-")

    plot_error(error_data[2], "Z Position Error against JPL for 2002 KL6: 0.0001 Time Step, 365 Days, 1e-9 rtol", "g-")

    plot_error(overall_error_data, "Position Magnitude Error against JPL for 2002 KL6: 0.0001 Time Step, 365 Days, 1e-9 rtol", "m-")

    plt.show()


#asteroid_2002_kl6_test_1yr()

asteroid_2002_kl6_test()





