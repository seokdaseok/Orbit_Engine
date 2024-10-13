import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Function to plot the 3D graph
def plot_graph():
    ax.clear()
    # Example data for a 3D scatter plot
    x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)
    ax.scatter(x, y, z)
    canvas.draw()

# Create the main application window
root = tk.Tk()
root.title("3D Graph Display")

# Create a matplotlib figure and axis
fig = Figure()
ax = fig.add_subplot(111, projection='3d')

# Create a canvas to display the matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

# Create a button to display the graph
button = ttk.Button(root, text="Display Graph", command=plot_graph)
button.pack(side=tk.BOTTOM)

# Run the tkinter main loop
root.mainloop()
