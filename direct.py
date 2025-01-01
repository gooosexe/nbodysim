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

def gforce(m1, m2, r):
    # calculate gravitational force between two bodies
    return G * m1 * m2 / (r ** 2 + SOFT_PARAM ** 2)

def simulate(bodies, sim_len):
    simulation = [np.array([body.pos for body in bodies])]
    for k in range(sim_len):
        for i in bodies:
            i.acc = np.array([0.0, 0.0])
            for j in bodies:
                if i != j:
                    r = np.linalg.norm(j.pos - i.pos)
                    # if bodies are at the same position, skip
                    if r == 0:
                        continue
                    r_dir = (j.pos - i.pos) / r
                    f = gforce(i.mass, j.mass, r)
                    acc = f / i.mass
                    i.acc += r_dir * acc
            i.update(DELTA, TSTEP)
        if k % 10 == 0:
            print("\033[H\033[J", end="")
            print(f"{k*100.0/float(sim_len)}% done")
        # update quadtree
        simulation.append(np.array([body.pos for body in bodies]))
    return np.array(simulation)

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
simulation = simulate(bodies, SIM_LEN)

fig = plt.figure()
scatter = plt.scatter([], [], s=1, c='black', vmin=-1e1, vmax=1e1)

ax = fig.get_axes()
ax[0].set_xlim(0, bound)
ax[0].set_ylim(0, bound)
ax[0].set_title(f'{BODIES} bodies equal masses and radii')
ax[0].set_xlabel('x (million km)')
ax[0].set_ylabel('y (million km)')

plt.gca().set_aspect('equal', adjustable='box') 

print('Simulation time:', time.time() - start_time)

print('Creating animation...')

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