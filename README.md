Orbit Engine Simulator! This package is intended to be easy to use by all. It uses ordinary differential equations (ODE's) to predict the orbital paths of any object with specified initial conditions. 

Orbit Engine is a tool designed in Python that uses second order differential equation solvers to 
simulate orbits for systems with multiple bodies. The tool used via a graphical user interface that
which allows users to input initial conditions for various orbital systems. Users can manually type
the initial positions (in 𝐴𝑈), velocities (in 𝐴𝑈/𝐷𝑎𝑦), and masses (in 𝑀☉) for their given celestial
bodies. Alternatively, users can pull initial conditions from a csv file stored on the users’ local
drive. Once imported into the tool, the user can configure the simulation settings. The user can
modify the time step, duration, and rtol for the ordinary differential equation solvers; the user can
also leave this field empty and use the tool’s default simulation settings. Once established, the user
can run the simulation. The simulation algorithm in this tool is efficient and accurate.

Once the simulation is finished running, users may plot the results and
view them on the embedded plot in the graphical user interface. The user may also choose to
animate the plot to view the orbits. The user can then save the orbit data as a csv file. The tool will
automatically split the data per day.

Dependencies:
- numpy
- matplotlib
- scipy
- customtkinter


