import matplotlib.pyplot as plt
from matplotlib import animation, colors, colormaps
import numpy as np
from structures import Body, QuadTree
import time

# Simulation scale:
# 1 pixel per million km
# mass in kg

# Test 1: simulation of 500 bodies with the same mass and radius
DELTA = 0.01 # 0.01 seconds per frame
TSTEP = 59220 # 10 week per frame 
SIM_SPEED = 1 # 1 steps per frame
SIM_LEN = 1000
G = 6.67430e-11
BODIES = 500 
MASS = 1e24 # 1 septillion kg, roughly 1/5 of earth
RADIUS = 1e6 # 1 million meters, roughly 1/6 of earth
SOFT_PARAM = 1e7 # softening parameter
TREE_UPDATE_FREQ = 10 # how many steps between quadtree updates
LINE_TOGGLE = False
NODE_DISTANCE_RATIO = 0.5
BODY_LIMIT = 2

def gforce(m1, m2, vec_r):
    # calculate gravitational force between two bodies
    #print(vec_r)
    r = np.linalg.norm(vec_r)
    #print(r)
    if r == 0:
        return np.array([0.0, 0.0])
    dir_r = vec_r / r
    force_mag = G * m1 * m2 / (r ** 2 + SOFT_PARAM ** 2)
    return force_mag * dir_r


def calculate_total_force(body, quadtree):
    if quadtree.get_ratio(body) < NODE_DISTANCE_RATIO:
        return gforce(body.mass, quadtree.get_total_mass(), quadtree.center_mass - body.pos)
    else:
        force = np.array([0.0, 0.0])
        for child in quadtree.children:
            force += calculate_total_force(body, child)
        return force
    

def simulate(bodies, sim_len):
    simulation = [np.array([body.pos for body in bodies])]
    tree_ev = []
    quadtree = QuadTree([0, 0, 1e9, 1e9], BODY_LIMIT, bodies)
    for k in range(sim_len):
        positions = []
        # calculate ratio for each body
        for body in bodies:
            body.acc = np.array([0.0, 0.0])
            body.acc = calculate_total_force(body, quadtree) / body.mass
            #print(f'acceleration: {body.acc}')
            body.update(DELTA, TSTEP)
            positions.append(body.pos)
            # traverse quadtree
        if k % 10 == 0:
            print("\033[H\033[J", end="")
            print(f"{k*100.0/float(sim_len)}% done")
        # update quadtree
        if k % TREE_UPDATE_FREQ == 0:
            quadtree = QuadTree([0, 0, 1e9, 1e9], BODY_LIMIT, bodies)
        tree_ev.append(quadtree)
        simulation.append(np.array(positions))
    return np.array(simulation), np.array(tree_ev)

start_time = time.time()

# create random bodies
bodies = []
for i in range(BODIES):
    # set random positions (m) and velocities (m s^-1)
    x = np.random.randint(0, 1e9)
    y = np.random.randint(0, 1e9)
    vx = np.random.randint(-1e3, 1e3)
    vy = np.random.randint(-1e3, 1e3)
    bodies.append(Body(np.array([x, y], dtype=float), np.array([vx, vy], dtype=float), MASS, RADIUS))

scale = 1e-6
bound = 1e9*scale
simulation, tree_ev = simulate(bodies, SIM_LEN)

fig = plt.figure()
scatter = plt.scatter([], [], s=1, c='black', vmin=-1e1, vmax=1e1)
line_data = []
for tree in tree_ev:
    line_data.append(tree.lines())

max_lines = max([len(lines) for lines in line_data])
lines = [plt.plot([], [], 'r-')[0] for _ in range(max_lines)]

ax = fig.get_axes()
ax[0].set_xlim(0, bound)
ax[0].set_ylim(0, bound)
ax[0].set_title(f'{BODIES} bodies equal masses and radii')
ax[0].set_xlabel('x (million km)')
ax[0].set_ylabel('y (million km)')

plt.gca().set_aspect('equal', adjustable='box') 

print('Simulation time:', time.time() - start_time)

print('Creating animation...')

if LINE_TOGGLE:
    def update(frame):
        scatter.set_offsets(simulation[frame*SIM_SPEED]*scale)
        current_data = line_data[frame]
        num_lines = len(current_data)

        for i in range(num_lines):
            x1, y1, x2, y2 = current_data[i]
            lines[i].set_data([x1*scale, x2*scale], [y1*scale, y2*scale])
            lines[i].set_visible(True)

        for i in range(num_lines, max_lines):
            lines[i].set_data([], [])
            lines[i].set_visible(False)

        return lines + [scatter]
else:
    def update(frame):
        scatter.set_offsets(simulation[frame*SIM_SPEED]*scale)
        return [scatter]

print('Frames:', SIM_LEN//SIM_SPEED)
print('Frames per second:', 1/(DELTA))
print(f'Timescale: {TSTEP*(1/DELTA)} seconds per second')
print('Animation length:', SIM_LEN//SIM_SPEED*50/1000, 'seconds')

print('Total time:', time.time() - start_time)

anim = animation.FuncAnimation(fig, update, frames=range(SIM_LEN//SIM_SPEED), interval=DELTA*1000, blit=True)

plt.show()
plt.close()