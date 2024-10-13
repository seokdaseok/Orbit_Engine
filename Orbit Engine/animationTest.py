import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np

# Create the main Tkinter window
root = tk.Tk()
root.title("Animation")

# Create a Matplotlib figure and axes
fig, ax = plt.subplots()

# Set up the plot limits
ax.set_xlim(0, 2*np.pi)
ax.set_ylim(-1, 1)

# Initialize the plot line
line, = ax.plot([], [], lw=2)

# Define the initialization function
def init():
    line.set_data([], [])
    return line,

# Define the animation function
def update(frame):
    x = np.linspace(0, 2*np.pi, 1000)
    y = np.sin(x + frame/10.0)
    line.set_data(x, y)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, init_func=init, frames=100, interval=50, blit=True)

# Embed the plot in Tkinter using FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Run the Tkinter event loop
root.mainloop()
