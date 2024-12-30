## Run This Script to run the GUI ##

## Default Simulation Settings:
#  - Timestep: 0.0001
#  - Duration: 365
#  - rtol: 1e-9

## Make sure to Import these Packages:

# numpy
# matplotlib
# scipy
# customtkinter

import GUI_Universal

# Initial Conditions Template 1: Sun at center with a massless planet 1 AU away at circular Orbit

# Body 1:
#  - Position: 0,0,0
#  - Velocity: 0,0,0
#  - Mass: 1

# Body 2:
#  - Position: 1,0,0
#  - Velocity: 0,0.01720209895,0
#  - Mass: 0


# Initial Conditions Template 2: Chaotic 3 Body System

# Body 1:
#  - Position: 1,0,0
#  - Velocity: 0,0.01720209895,0
#  - Mass: 0.5

# Body 2:
#  - Position: 0,0,0
#  - Velocity: 0.013,0, 0
#  - Mass: 1

# Body 3:
#  - Position: 0,0.5,0
#  - Velocity: -0.013,0,0
#  - Mass: 0.8


# Initial Conditions Template 3: Binary Star System

# Body 1:
#  - Position: 0.5,0,0
#  - Velocity: 0,0.02,0
#  - Mass: 2

# Body 2:
#  - Position: -0.5,0,0
#  - Velocity: 0,-0.02,0
#  - Mass: 2

# Initial Conditions Template 4: Earth-Moon system with initial conditions obtained from JPL Horizons

# Body 1 (Sun):
#  - Position: -8.460896220635403E-03, -2.051987493506281E-03,  2.142063120055386E-04
#  - Velocity: 3.742878545157929E-06, -8.016443961813632E-06, -1.959599174187973E-08
#  - Mass: 1

# Body 2 (Earth):
#  - Position: 9.718258485791090306e-01,-2.333943905187164936e-01,2.172948571505989085e-04
#  - Velocity: 3.681039806474151882e-03,1.667393004745482132e-02,-1.012334391669507924e-06
#  - Mass: 3.002739999999999901e-06

# Body 3 (Moon):
#  - Position: 9.708467499202165e-01, -2.308954378088815e-01,  4.592622665659554e-04
#  - Velocity: 3.152309495502472e-03,  1.648418836072312e-02,  3.936099841060578e-06
#  - Mass: 3.689999999999999955e-08