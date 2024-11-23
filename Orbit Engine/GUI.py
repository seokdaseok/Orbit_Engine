import tkinter as tk
from tkinter import ttk
import threading
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import run
import initial
import pullPlanets

import time

#0.000003

##Functions that the GUI will actually use

finished_run = False

sim_time_step = 0.01 # 0.0001
sim_duration = 365 
sim_rtol = 1e-4 #1e-9

# sim_time_step = 1000.0
# sim_duration = 20.0

def run_simulation():

    if(len(initial.listOfPlanetsInScene) < 1):
        console_text_box_label.config(text="No objects currently exist. Try Adding one! You can generate them or import them from a CSV.")
    else:
        console_text_box_label.config(text="Running...")

        generate_planet_button["state"] = "disabled"
        run_button["state"] = "disabled"
        csv_planet_button["state"] = "disabled"
        sim_settings_planet_button["state"] = "disabled"

        run.set_conditions(sim_time_step, sim_duration, sim_rtol)

        t = threading.Thread(target=run.run_thing)

        t.start()

        check_if_done(t)

def check_if_done(t):

    if not t.is_alive():
        finish_string = "Finished! Completed in " + str(run.run_time_taken) + " Seconds"

        console_text_box_label.config(text=finish_string)
        run_button["state"] = "normal"
        generate_planet_button["state"] = "normal"
        run_button["state"] = "normal"
        csv_planet_button["state"] = "normal"
        sim_settings_planet_button["state"] = "normal"
    else:
        console_text_box_label.config(text="Running...")
        schedule_check(t)

def schedule_check(t):

    root.after(500, check_if_done, t)


def button_click_test():
    console_text_box_label.config(text="This Button Works")

def config_sim_settings():
    sim_settings_string = sim_settings_text_box.get("1.0", tk.END).strip()

    try:    
        sim_settings = [float(x) for x in sim_settings_string.split(',')]
        global sim_time_step
        sim_time_step = sim_settings[0]
        global sim_duration
        sim_duration = sim_settings[1]
        global sim_rtol
        sim_rtol = sim_settings[2]

        console_text_box_label.config(text="Simulation Settings Changed!")
    except ValueError:
        console_text_box_label.config(text="Value Error! Make sure the inputted format is correct")
    except TypeError:
        console_text_box_label.config(text="Value Error! Make sure the inputted format is correct")

def reset_simulation_method():
    initial.listOfPlanetsInScene.clear()

    ##print(initial.listOfPlanetsInScene)

    console_text_box_label.config(text="Simulation Cleared")


def generate_planet_method():
    pos_value = position_text_box.get("1.0", tk.END).strip()
    vel_value = velocity_text_box.get("1.0", tk.END).strip()
    mass_value = mass_text_box.get("1.0", tk.END).strip()

    try:
        initial.generatePlanetFromString(pos_value, vel_value, mass_value)
        console_text_box_label.config(text="Sucessfully Generated!")
    except ValueError:
        console_text_box_label.config(text="Value Error. Make sure you are inputting the values in the correct format")
    except TypeError:
        console_text_box_label.config(text="Type Error. Make sure you are inputting the values in the correct format")

def plot_results_method():

    run.get_results()

    if len(run.planet_position_data) >= 1:

        ax.clear()

        N = run.planet_list_count

        for i in range(N):

            ax.plot(run.planet_position_data[i, 0, ::25], run.planet_position_data[i, 1, ::25], run.planet_position_data[i, 2, ::25])


        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_zlim(-2, 2)

        # ax.set_xlim(-0.004, 0.004)
        # ax.set_ylim(-0.004, 0.004)
        # ax.set_zlim(-0.004, 0.004)

        ax.set_aspect('equal')

        # for planet_positions in run.planet_position_data:
        #     x_cords = planet_positions[:, 0]
        #     y_cords = planet_positions[:, 1]
        #     z_cords = planet_positions[:, 2]

        #     print(x_cords)

        #     ax.plot(x_cords, y_cords, z_cords)
            
        canvas.draw()
        console_text_box_label.config(text="Successfully plotted!")

    else:
        console_text_box_label.config(text="No Position Data yet.")

def pull_planets_method():
    directory_to_planets = csv_text_box.get("1.0", tk.END).strip()

    initial.listOfPlanetsInScene = pullPlanets.pull_planets(directory_to_planets)

    console_text_box_label.config(text="Successfully added csv planets to simulation")

def save_planets_to_csv_method():
    directory_to_planets = csv_text_box.get("1.0", tk.END).strip()

    pullPlanets.create_planet_csv(initial.listOfPlanetsInScene, directory_to_planets)

    console_text_box_label.config(text="Successfully added simulation planets to csv")



page_background_color = "#E3E1D9"
input_background_color = "#F2EFE5"

bottom_page_background_color = "#C7C8CC"

# Create the main window
root = tk.Tk()
root.title("Orbit Engine")

# Set the window properties
root.geometry("1920x1080")

root.grid_rowconfigure(0, weight=5)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Create the left frame
left_frame = tk.Frame(root, bg=page_background_color)
left_frame.grid(row=0, column=0, sticky="nsew")

# Create the right frame
right_frame = tk.Frame(root, bg=page_background_color)
right_frame.grid(row=0, column=1, sticky="nsew")

# Create the bottom frame
bottom_frame = tk.Frame(root, bg=bottom_page_background_color)
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_rowconfigure(1, weight=4)
bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=1)
bottom_frame.grid_columnconfigure(2, weight=1)

bottom_frame_top = tk.Frame(bottom_frame, bg=bottom_page_background_color)
bottom_frame_top.grid(row=0, column=0, columnspan=3, sticky="nsew")

bottom_frame_left = tk.Frame(bottom_frame, bg=bottom_page_background_color)
bottom_frame_left.grid(row=1, column=0, sticky="nsew")

bottom_frame_center = tk.Frame(bottom_frame, bg=bottom_page_background_color)
bottom_frame_center.grid(row=1, column=1, sticky="nsew")

bottom_frame_right = tk.Frame(bottom_frame, bg=bottom_page_background_color)
bottom_frame_right.grid(row=1, column=2, sticky="nsew")


# Create a figure for the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Add a title to the plot
ax.set_title('Simulation Space')

# Create a title label for the application
title_label = tk.Label(left_frame, text="Orbit Engine Simulator", font=('Callibri', 32, 'bold'), pady=8, bg=page_background_color)
title_label.pack(side=tk.TOP, fill=tk.X)

# Embed the plot in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

##Using the Orbit Engine
##instructionsText = """Orbit Engine is a tool developed to simulate and graph orbital mechanics easily. \n \n Features:\n \n Generate planets manually, Add planets with CSV, Swap between Basic and ODE, Change time step, Change Duration, Save Data of Orbits, Save data of Initial Conditions, Plot Results from Previous, Plot Results from CSV Saved, Animate Results from Previous, Animate Results from CSV"""

instruction_text_box = tk.Text(master=left_frame, height=0.5, width=25, bg=page_background_color, bd=0)
instruction_text_box.pack(fill=tk.BOTH, expand=False, padx=25)
instruction_text_box.config(state=tk.DISABLED)
instruction_text_box.tag_configure('center', justify='center')
instruction_text_box.tag_add('center', '1.0', 'end')

##position text box stuff
position_text_box_label = tk.Label(left_frame, text="Position (AU)", font=('Callibri', 12, 'bold'), pady=3, bg=page_background_color)
position_text_box_label.pack(side=tk.TOP, fill=tk.X)

position_text_box = tk.Text(master=left_frame, height=1.5, width=25, bg=input_background_color, bd=0)
position_text_box.pack(fill=tk.BOTH, expand=False, padx=50, pady=10)
position_text_box.insert(tk.END, "Input position vector in the form x,y,z")


##velocity textbox stuff
velocity_text_box_label = tk.Label(left_frame, text="Velocity (AU/Day)", font=('Callibri', 12, 'bold'), pady=3, bg=page_background_color)
velocity_text_box_label.pack(side=tk.TOP, fill=tk.X)

velocity_text_box = tk.Text(master=left_frame, height=1.5, width=25, bg=input_background_color, bd=0)
velocity_text_box.pack(fill=tk.BOTH, expand=False, padx=50, pady=10)
velocity_text_box.insert(tk.END, "Input velocity vector in the form x,y,z")


##mass textbox stuff
mass_text_box_label = tk.Label(left_frame, text="Mass (Solar Masses)", font=('Callibri', 12, 'bold'), pady=3, bg=page_background_color)
mass_text_box_label.pack(side=tk.TOP, fill=tk.X)

mass_text_box = tk.Text(master=left_frame, height=1.5, width=25, bg=input_background_color, bd=0)
mass_text_box.pack(fill=tk.BOTH, expand=False, padx=50, pady=10)
mass_text_box.insert(tk.END, "Input mass of planet relative to solar masses (mass of the sun = 1)")

##generate planet button stuff

generate_planet_button = tk.Button(
    master=left_frame,
    text="Generate Planet",
    command=generate_planet_method,
    font=("Callibri", 12, 'bold'),
    width=15,
    height=1,
    bg="#96C9F4", ##Pale Blue Color
    bd=2,
    relief=tk.SOLID
)

generate_planet_button.pack(side=tk.TOP, padx=15, pady=15)

##Add from CSV stuff
csv_text_box_label = tk.Label(left_frame, text="Add Planets from CSV", font=('Callibri', 12, 'bold'), pady=3, bg=page_background_color)
csv_text_box_label.pack(side=tk.TOP, fill=tk.X)

csv_text_box = tk.Text(master=left_frame, height=1.5, width=25, bg=input_background_color, bd=0)
csv_text_box.pack(fill=tk.BOTH, expand=False, padx=50, pady=10)
csv_text_box.insert(tk.END, "earth_moon.csv")

csv_planet_button = tk.Button(
    master=left_frame,
    text="Pull Planets from CSV",
    command=pull_planets_method,
    font=("Callibri", 12, 'bold'),
    width=20,
    height=1,
    bg="#9CDBA6", ##Pale Green Color
    bd=2,
    relief=tk.SOLID
)

csv_planet_button.pack(side=tk.TOP, padx=15, pady=15)

csv_planet_button = tk.Button(
    master=left_frame,
    text="Add Planets to CSV",
    command=save_planets_to_csv_method,
    font=("Callibri", 12, 'bold'),
    width=20,
    height=1,
    bg="#A6AEBF", ##Pale Green Color
    bd=2,
    relief=tk.SOLID
)

csv_planet_button.pack(side=tk.TOP, padx=15, pady=15)

##Configure Simulation Settings

sim_settings_text_box_label = tk.Label(left_frame, text="Configure Simulation Settings", font=('Callibri', 12, 'bold'), pady=3, bg=page_background_color)
sim_settings_text_box_label.pack(side=tk.TOP, fill=tk.X)

sim_settings_text_box = tk.Text(master=left_frame, height=1.5, width=25, bg=input_background_color, bd=0)
sim_settings_text_box.pack(fill=tk.BOTH, expand=False, padx=50, pady=10)
sim_settings_text_box.insert(tk.END, "Input simulation settings in this form: time step,duration")

sim_settings_planet_button = tk.Button(
    master=left_frame,
    text="Configure Simulation Settings",
    command=config_sim_settings,
    font=("Callibri", 12, 'bold'),
    width=30,
    height=1,
    bg="#F9D689", ##Pale Green Color
    bd=2,
    relief=tk.SOLID
)

sim_settings_planet_button.pack(side=tk.TOP, padx=15, pady=15)

##reset button

reset_settings_planet_button = tk.Button(
    master=left_frame,
    text="Reset Simulation",
    command=reset_simulation_method,
    font=("Callibri", 12, 'bold'),
    width=30,
    height=1,
    bg="#C5705D", ##Pale Green Color
    bd=2,
    relief=tk.SOLID
)

reset_settings_planet_button.pack(side=tk.TOP, padx=15, pady=15)

##console stuff

console_text_box_label = tk.Label(bottom_frame_top, text="No Errors", font=('Callibri', 12, 'bold'), fg='white', pady=5, bg="black")
console_text_box_label.pack(side=tk.TOP, fill=tk.X)

##run button stuff
run_button = tk.Button(
    master=bottom_frame_left, 
    text="Run Simulation", 
    command=run_simulation, 
    font=("Callibri", 18, 'bold'),
    width=40, 
    height=3, 
    bg='#FFCCCB',  # Pale red color
    bd=2,          # Soft border width
    relief=tk.SOLID # Solid border style
)
run_button.pack(fill=tk.Y, padx=65, pady=15)
##run_button.pack(pady=45, padx=45, side=tk.TOP)

##display path button stuff
show_button = tk.Button(
    master=bottom_frame_center, 
    text="Plot Results", 
    command=plot_results_method, 
    font=("Callibri", 18, 'bold'),
    width=40, 
    height=3, 
    bg='#E68369',  # Pale Orange color
    bd=2,          # Soft border width
    relief=tk.SOLID # Solid border style
)
show_button.pack(fill=tk.Y, padx=65, pady=15)

##animate button stuff
animate_button = tk.Button(
    master=bottom_frame_right, 
    text="Animate Results", 
    command=button_click_test, 
    font=("Callibri", 18, 'bold'),
    width=40, 
    height=3, 
    bg='#7776B3',  # Pale purple color
    bd=2,          # Soft border width
    relief=tk.SOLID # Solid border style
)

animate_button.pack(fill=tk.Y, padx=65, pady=15)

# Start the Tkinter event loop
root.mainloop()
