import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import threading
import numpy as np

import run
import initial
import pullPlanets

import time

# CustomTkinter setup
ctk.set_appearance_mode("light")  # Modes: "System" (default), "Light", "Dark"
ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (default), "green", "dark-blue"

finished_run = False

sim_time_step = 0.0001 # 0.0001
sim_duration = 365 
sim_rtol = 1e-9 #1e-9

animation_interval = 50

animation_splice_factor = 1

tracked_planet_index = -1

def run_simulation():

    #print("hi")

    if(len(initial.listOfPlanetsInScene) < 1):
        console_text_box_label.configure(text="No objects currently exist. Try Adding one! You can generate them or import them from a CSV.")
    else:
        console_text_box_label.configure(text="Running...")

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

        console_text_box_label.configure(text=finish_string)
        run_button["state"] = "normal"
        generate_planet_button["state"] = "normal"
        run_button["state"] = "normal"
        csv_planet_button["state"] = "normal"
        sim_settings_planet_button["state"] = "normal"
    else:
        console_text_box_label.configure(text="Running...")
        schedule_check(t)

def schedule_check(t):

    root.after(500, check_if_done, t)

def plot_results_method():

    ax.clear()
    global tracked_planet_index
    tracked_planet_index = -1
    run.get_results()

    if len(run.planet_position_data) >= 1:

        masses = np.array(initial.listOfPlanetsInScene)[:,6] #TO DO: assuming that this is in the same order as planet position data, need to check later

        ax.clear()

        N = run.planet_list_count

        for i in range(N):

            nth = int((1 / sim_time_step) / 25)

            ax.plot(run.planet_position_data[i, 0, ::nth], run.planet_position_data[i, 1, ::nth], run.planet_position_data[i, 2, ::nth], "-", label=masses[i])


        graph_dist = run.largest_dist * 1.1
        
        ax.set_xlim(-graph_dist, graph_dist)
        ax.set_ylim(-graph_dist, graph_dist)
        ax.set_zlim(-graph_dist, graph_dist)

        ax.set_aspect('equal')

        ax.legend(fontsize=4, loc='upper left', bbox_to_anchor=(1, 1))
            
        canvas.draw()
        console_text_box_label.configure(text="Successfully plotted!")

    else:
        console_text_box_label.configure(text="No Position Data yet.")

def toggle_track_planet():
    global tracked_planet_index

    if len(run.planet_position_data) == 0:
        console_text_box_label.configure(text="No Position Data yet. Run a simulation first!")
        return

    num_planets = len(run.planet_position_data)
    tracked_planet_index = (tracked_planet_index + 1)  # Cycle through planets and wide view

    if(tracked_planet_index == num_planets):
        tracked_planet_index = -1

    masses = [float(planet[6]) for planet in initial.listOfPlanetsInScene]

    if tracked_planet_index == -1:  # Wide view
        console_text_box_label.configure(text="Currently in wide view.")
    else:  # Following a specific planet
        console_text_box_label.configure(text=f"Currently following: {masses[tracked_planet_index]:.2e} M\u2609")

def animate_results():
    ax.clear()
    

    global tracked_planet_index
    tracked_planet_index = -1

    global animation_splice_factor

    if len(run.planet_position_data) == 0:
        console_text_box_label.configure(text="No Position Data yet. Run a simulation first!")
        return

    # Clear the current plot
    #ax.set_title('Simulation Space')

    graph_dist = run.largest_dist * 1.1

    ax.set_xlim(-graph_dist, graph_dist)
    ax.set_ylim(-graph_dist, graph_dist)
    ax.set_zlim(-graph_dist, graph_dist)
    ax.set_aspect('auto')

    # Prepare data for animation
    planet_positions = run.planet_position_data  # Shape: (N, 3, time_steps)
    nth = int(1 / (sim_time_step * animation_splice_factor))  # Subsample factor
    subsampled_positions = planet_positions[:, :, ::nth]  # Take every nth frame
    num_frames = subsampled_positions.shape[2]  # Number of frames after subsampling
    num_planets = subsampled_positions.shape[0]

    # Get planet masses (assuming the masses are stored in the same order)
    masses = [float(planet[6]) for planet in initial.listOfPlanetsInScene]

    # Initialize trails, spheres, labels for each planet, and a time label
    trails = [ax.plot([], [], [], "-")[0] for i in range(num_planets)]
    spheres = [ax.scatter([], [], [], s=15, label=f"Mass: {masses[i]:.2e} M☉") for i in range(num_planets)]
    labels = [ax.text(0, 0, 0, f"{masses[i]:.2e} M☉", color="black") for i in range(num_planets)]
    time_label = ax.text2D(0.05, 0.95, "", transform=ax.transAxes, fontsize=12, color="black")

    def update(frame):

        if(tracked_planet_index != -1):

            #if tracking

            t = (frame + 1) / animation_splice_factor  # Time starts at t=1
            time_label.set_text(f"Time: {t}")

            #graph_dist = run.largest_dist * 1.1

            x_current, y_current, z_current = subsampled_positions[tracked_planet_index, :, frame]
            #print(x_current, y_current, z_current)
            ax.set_xlim(x_current - graph_dist / 10, x_current + graph_dist / 10)
            ax.set_ylim(y_current - graph_dist / 10, y_current + graph_dist / 10)
            ax.set_zlim(z_current - graph_dist / 10, z_current + graph_dist / 10)
            ax.set_aspect('auto')

            for i, (trail, sphere, label) in enumerate(zip(trails, spheres, labels)):
                # Get current and trail data
                x_trail, y_trail, z_trail = subsampled_positions[i, :, :frame]
                x_current, y_current, z_current = subsampled_positions[i, :, frame - 1]

                # Update the trail
                trail.set_data(x_trail, y_trail)
                trail.set_3d_properties(z_trail)

                # Update the sphere
                sphere._offsets3d = ([x_current], [y_current], [z_current])

                # Update the label
                label.set_position((x_current, y_current))
                label.set_3d_properties(z_current)
                label.set_text(f"{masses[i]:.2e} M☉")
            return trails + spheres + labels + [time_label]
        
        else:
            # ax.set_xlim(-graph_dist, graph_dist)
            # ax.set_ylim(-graph_dist, graph_dist)
            # ax.set_zlim(-graph_dist, graph_dist)
            # ax.set_aspect('auto')

            # if not tracking
            t = (frame + 1) / animation_splice_factor  # Time starts at t=1
            time_label.set_text(f"Time: {t}")

            for i, (trail, sphere, label) in enumerate(zip(trails, spheres, labels)):
                # Get current and trail data
                x_trail, y_trail, z_trail = subsampled_positions[i, :, :frame]
                x_current, y_current, z_current = subsampled_positions[i, :, frame - 1]

                # Update the trail
                trail.set_data(x_trail, y_trail)
                trail.set_3d_properties(z_trail)

                # Update the sphere
                sphere._offsets3d = ([x_current], [y_current], [z_current])

                # Update the label
                label.set_position((x_current, y_current))
                label.set_3d_properties(z_current)
                label.set_text(f"{masses[i]:.2e} M☉")
            return trails + spheres + labels + [time_label]

    # Create the animation
    ani = FuncAnimation(fig, update, frames=num_frames, interval=animation_interval, blit=False)

    ax.legend(fontsize=4, loc='upper left', bbox_to_anchor=(1, 1))
    canvas.draw()
    console_text_box_label.configure(text="Animation Complete!")

def generate_planet_method():
    pos_value = position_entry.get()
    vel_value = velocity_entry.get()
    mass_value = mass_entry.get()

    try:
        initial.generatePlanetFromString(pos_value, vel_value, mass_value)
        console_text_box_label.configure(text="Sucessfully Generated!")
    except ValueError:
        console_text_box_label.configure(text="Value Error. Make sure you are inputting the values in the correct format")
    except TypeError:
        console_text_box_label.configure(text="Type Error. Make sure you are inputting the values in the correct format")

def pull_planets_method():
    directory_to_planets = csv_entry.get()

    initial.listOfPlanetsInScene = pullPlanets.pull_planets(directory_to_planets)

    console_text_box_label.configure(text="Successfully added csv planets to simulation")

def save_planets_to_csv_method():
    directory_to_planets = csv_entry.get()

    pullPlanets.create_planet_csv(initial.listOfPlanetsInScene, directory_to_planets)

    console_text_box_label.configure(text="Successfully added simulation planets to csv")

def config_sim_settings():
    sim_settings_string = sim_settings_entry.get()

    try:    
        sim_settings = [float(x) for x in sim_settings_string.split(',')]
        global sim_time_step
        sim_time_step = sim_settings[0]
        global sim_duration
        sim_duration = sim_settings[1]
        global sim_rtol
        sim_rtol = sim_settings[2]

        console_text_box_label.configure(text="Simulation Settings Changed!")
    except ValueError:
        console_text_box_label.configure(text="Value Error! Make sure the inputted format is correct")
    except TypeError:
        console_text_box_label.configure(text="Value Error! Make sure the inputted format is correct")

def save_orbits_to_csv_method():
    #masses = np.array(initial.listOfPlanetsInScene)[:,6]

    # nth = int(1 / sim_time_step)
    # print("Nth:", nth)

    # the_position_data = run.planet_position_data * (run.ODE.nu /1.496e11) #position
    # the_velocity_data = run.planet_velocity_data * (run.ODE.nu /1.496e11) #velocity

    if(run.planet_position_data.size == 0):
        console_text_box_label.configure(text="No orbit data yet")
    else:

        masses = np.array(initial.listOfPlanetsInScene)[:,6]

        nth = int(1 / sim_time_step)
        print("Nth:", nth)

        the_position_data = run.planet_position_data * (run.ODE.nu /1.496e11) #position
        the_velocity_data = run.planet_velocity_data * (run.ODE.nu /1.496e11) #velocity

        the_directory = save_orbit_entry.get()

        print("Shape of Data Array:", the_position_data.shape[0])
        for i in range(the_position_data.shape[0]):
            real_directory = the_directory[:-4] + "_" + str(masses[i]) + "_M_sun.csv"
            print("The Directory", real_directory)
            the_real_data = np.concatenate((the_position_data[i, :, ::nth], the_velocity_data[i, :, ::nth])).T #np.transpose(the_data[i, 0:6, ::nth])
            
            print("Shape of the real data:", the_real_data.shape)
            np.savetxt(real_directory, the_real_data, delimiter=",")

        console_text_box_label.configure(text="Successfully saved data!")

def change_frame_rate():
    animation_settigns_string = animation_settings_entry.get()

    try:
        animation_settings = [float(x) for x in animation_settigns_string.split(',')]
        frame_duration = animation_settings[0]
        splice_factor = animation_settings[1]

        global animation_interval
        global animation_splice_factor

        animation_interval = frame_duration
        animation_splice_factor = splice_factor

        console_text_box_label.configure(text="Sucessfully Changed Animation Settings!")
    except TypeError:
        console_text_box_label.configure(text="Value Error. Make sure you are inputting the values in the correct format")

def reset_simulation_method():
    initial.listOfPlanetsInScene = []

    ##print(initial.listOfPlanetsInScene)

    console_text_box_label.configure(text="Simulation Cleared")

# Main application window
root = ctk.CTk()
root.title("Orbit Engine Simulator")
root.geometry("1600x1000")

# Configure grid layout
root.grid_rowconfigure(0, weight=5)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Create frames
left_frame = ctk.CTkFrame(root, corner_radius=0)
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

right_frame = ctk.CTkFrame(root, corner_radius=0)
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

bottom_frame = ctk.CTkFrame(root, corner_radius=0)
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

# Configure bottom frame layout
bottom_frame.grid_rowconfigure(0, weight=1)
bottom_frame.grid_rowconfigure(1, weight=4)
bottom_frame.grid_columnconfigure(0, weight=1)
bottom_frame.grid_columnconfigure(1, weight=1)
bottom_frame.grid_columnconfigure(2, weight=1)

# Bottom subframes
bottom_frame_top = ctk.CTkFrame(bottom_frame, corner_radius=0)
bottom_frame_top.grid(row=0, column=0, columnspan=3, sticky="nsew")

bottom_frame_left = ctk.CTkFrame(bottom_frame, corner_radius=0)
bottom_frame_left.grid(row=1, column=0, sticky="nsew")

bottom_frame_center = ctk.CTkFrame(bottom_frame, corner_radius=0)
bottom_frame_center.grid(row=1, column=1, sticky="nsew")

bottom_frame_right = ctk.CTkFrame(bottom_frame, corner_radius=0)
bottom_frame_right.grid(row=1, column=2, sticky="nsew")

left_scrollable_frame = ctk.CTkScrollableFrame(left_frame, width=300, height=600, corner_radius=0)
left_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

right_scrollable_frame = ctk.CTkScrollableFrame(right_frame, width=900, corner_radius=0)
right_scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Add title label
title_label = ctk.CTkLabel(left_scrollable_frame, text="Orbit Engine Simulator", font=ctk.CTkFont(size=32, weight="bold"))
title_label.pack(pady=10)

# Matplotlib figure for the right frame
fig = plt.figure(figsize=(6, 3.65))  # Smaller size for the plot
ax = fig.add_subplot(111, projection='3d')
#fig.dpi = 500
#ax.set_facecolor("#d3d3d3")
#ax.set_title("Simulation Space")
canvas = FigureCanvasTkAgg(fig, master=right_scrollable_frame)
canvas.get_tk_widget().pack(fill="both", expand=True)
toolbar_frame = ctk.CTkFrame(right_scrollable_frame, fg_color="#FFFDF0")
toolbar_frame.pack(fill="both", padx=10, pady=5)
toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
toolbar.update()
canvas.draw()

# Inputs and buttons in the left frame
position_label = ctk.CTkLabel(left_scrollable_frame, text="Position (AU):")
position_label.pack(pady=5)
position_entry = ctk.CTkEntry(left_scrollable_frame, placeholder_text="x, y, z", width=300)
position_entry.pack(pady=5)

velocity_label = ctk.CTkLabel(left_scrollable_frame, text="Velocity (AU/Day):")
velocity_label.pack(pady=5)
velocity_entry = ctk.CTkEntry(left_scrollable_frame, placeholder_text="x, y, z", width=300)
velocity_entry.pack(pady=5)

mass_label = ctk.CTkLabel(left_scrollable_frame, text="Mass (Solar Masses):")
mass_label.pack(pady=5)
mass_entry = ctk.CTkEntry(left_scrollable_frame, placeholder_text="Mass of planet relative to the Sun", width=300)
mass_entry.pack(pady=5)

generate_planet_button = ctk.CTkButton(left_scrollable_frame, text="Generate Planet", command=generate_planet_method, fg_color="#96C9F4", text_color="black")
generate_planet_button.pack(pady=10)

csv_label = ctk.CTkLabel(left_scrollable_frame, text="Add Planets from CSV:")
csv_label.pack(pady=5)
csv_entry = ctk.CTkEntry(left_scrollable_frame, placeholder_text="File Path (e.g solar_system.csv)", width=300)
csv_entry.pack(pady=5)

csv_planet_button = ctk.CTkButton(left_scrollable_frame, text="Pull Planets from CSV", command=pull_planets_method, fg_color="#9CDBA6", text_color="black")
csv_planet_button.pack(pady=10)

save_csv_button = ctk.CTkButton(left_scrollable_frame, text="Save Planets to CSV", command=save_planets_to_csv_method, fg_color="#A6AEBF", text_color="black")
save_csv_button.pack(pady=10)

sim_settings_label = ctk.CTkLabel(left_scrollable_frame, text="Configure Simulation Settings")
sim_settings_label.pack(pady=5)
sim_settings_entry = ctk.CTkEntry(left_scrollable_frame, placeholder_text="time step, duration (days), rtol", width=300)
sim_settings_entry.pack(pady=5)

sim_settings_planet_button = ctk.CTkButton(left_scrollable_frame, text="Confirm Simulation Settings", command=config_sim_settings, fg_color="#F9D689", text_color="black")
sim_settings_planet_button.pack(pady=10)

save_orbit_label = ctk.CTkLabel(left_scrollable_frame, text="Save Orbit to CSV")
save_orbit_label.pack(pady=5)
save_orbit_entry = ctk.CTkEntry(left_scrollable_frame, placeholder_text="File Path (e.g orbit_data.csv)", width=300)
save_orbit_entry.pack(pady=5)

save_orbit_button = ctk.CTkButton(left_scrollable_frame, text="Save Orbit to CSV", command=save_orbits_to_csv_method, fg_color="#C5705D", text_color="black")
save_orbit_button.pack(pady=10)

animation_settings_label = ctk.CTkLabel(left_scrollable_frame, text="Configure Animation Settings")
animation_settings_label.pack(pady=5)
animation_settings_entry = ctk.CTkEntry(left_scrollable_frame, placeholder_text="Frame Duration, Data split", width=300)
animation_settings_entry.pack(pady=5)

animation_settings_button = ctk.CTkButton(left_scrollable_frame, text="Confirm Animation Settings", command=change_frame_rate, fg_color="#5DB996", text_color="black")
animation_settings_button.pack(pady=10)

track_button = ctk.CTkButton(left_scrollable_frame, text="Track Planet in Animation", command=toggle_track_planet, fg_color="#FFD700", text_color="black")
track_button.pack(pady=10)

reset_button = ctk.CTkButton(left_scrollable_frame, text="Reset Simulation", command=reset_simulation_method, fg_color="#D6CFB4", text_color="black")
reset_button.pack(pady=10)

quit_button = ctk.CTkButton(left_scrollable_frame, text="Quit", command=root.destroy, fg_color="#FF6666", text_color="white")
quit_button.pack(pady=10)


# Console output in bottom frame
console_text_box_label = ctk.CTkLabel(bottom_frame_top, text="No Errors", font=ctk.CTkFont(size=14))
console_text_box_label.pack(pady=5)

# Buttons in bottom subframes
run_button = ctk.CTkButton(bottom_frame_left, text="Run Simulation", command=run_simulation, height=60, fg_color="#FFCCCB", text_color="black")
run_button.pack(pady=15, padx=15)

plot_button = ctk.CTkButton(bottom_frame_center, text="Plot Results", command=plot_results_method, height=60, fg_color="#E68369", text_color="black")
plot_button.pack(pady=15, padx=15)

animate_button = ctk.CTkButton(bottom_frame_right, text="Animate Results", command=animate_results, height=60, fg_color="#7776B3", text_color="black")
animate_button.pack(pady=15, padx=15)



# Start main loop
root.mainloop()