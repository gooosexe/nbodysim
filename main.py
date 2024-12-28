import matplotlib.pyplot as plt
from matplotlib import animation, colors, colormaps
import numpy as np
from structures import Body, QuadTree

# Simulation scale:
# 1 pixel per million km
# mass in kg

# Test 1: simulation of 500 bodies with the same mass and radius
TSTEP = 1e3 # 1 million seconds per step
SIM_SPEED = 1 # 8 steps per frame
SIM_LEN = 1
G = 6.67430e-11
BODIES = 100
MASS = 1e24 # 1 septillion kg, roughly 1/5 of earth
RADIUS = 1e6 # 1 million meters, roughly 1/6 of earth
SOFT_PARAM = 1e7 # softening parameter

def gforce(m1, m2, r):
    # calculate gravitational force between two bodies
    return G * m1 * m2 / (r ** 2 + SOFT_PARAM ** 2)

def simulate(bodies, tstep, sim_len):
    simulation = [np.array([body.pos for body in bodies])]
    for k in range(sim_len):
        for i in bodies:
            for j in bodies:
                if i != j:
                    # calculate norm of distance vector
                    r = np.linalg.norm(j.pos - i.pos)
                    if r == 0:
                        continue
                    norm_r = (j.pos - i.pos) / r
                    # calculate gravitational force
                    f = gforce(i.mass, j.mass, r)
                    # calculate acceleration
                    acc = f / i.mass
                    # update velocities for body i
                    i.vel += acc * norm_r * tstep
                    #state[i, 2:] += acc * (state[j, :2] - state[i, :2]) / r
            i.pos += i.vel * tstep
        if k % 10 == 0:
            print(f"{k*100/sim_len}% done")
        simulation.append(np.array([body.pos for body in bodies]))
    return np.array(simulation)

def construct_quadtree(bodies):
    # construct quadtree
    boundary = [0, 0, 1e9, 1e9]
    quadtree = QuadTree(boundary, 1)
    for body in bodies:
        quadtree.insert(body)
    return quadtree

def return_quadtree_lines(quadtree):
    x, y, width, height = quadtree.boundary
    lines = []
    if quadtree.children == []:
        x, y, width, height = quadtree.boundary
        lines.append((x, y, x + width, y))
        lines.append((x, y, x, y + height))
        lines.append((x + width, y, x + width, y + height))
        lines.append((x, y + height, x + width, y + height))
        return lines
    else:
        lines.append((x, y, x + width, y))
        lines.append((x, y, x, y + height))
        lines.append((x + width, y, x + width, y + height))
        lines.append((x, y + height, x + width, y + height))
        for child in quadtree.children:
            lines.extend(return_quadtree_lines(child))
        return lines

state = np.zeros((BODIES, 4)) # x, y, vx, vy for each body
bodies = []
for i in range(BODIES):
    # set random positions (m) and velocities (m s^-1)
    x = np.random.randint(0, 1e9)
    y = np.random.randint(0, 1e9)
    vx = np.random.randint(-1e3, 1e3)
    vy = np.random.randint(-1e3, 1e3)
    state[i] = [x, y, vx, vy]
    bodies.append(Body(np.array([x, y], dtype=float), np.array([vx, vy], dtype=float), MASS, RADIUS))
quadtree = construct_quadtree(bodies)

scale = 1e-6
bound = 1e9*scale
simulation = simulate(bodies, TSTEP, SIM_LEN)
print(f'{quadtree.count()} nodes in quadtree')

fig = plt.figure()
#scatter = plt.scatter([], [], s=1, c='black', vmin=-1e1, vmax=1e1)
scatter = plt.scatter(simulation[0][:, 0]*scale, simulation[0][:, 1]*scale, s=1, c='black')
for x1, y1, x2, y2 in return_quadtree_lines(quadtree):
    plt.plot([x1*scale, x2*scale], [y1*scale, y2*scale], 'r-')
ax = fig.get_axes()
ax[0].set_xlim(0, bound)
ax[0].set_ylim(0, bound)
#ax[0].set_title('500 bodies equal masses and radii')
ax[0].set_xlabel('x (million km)')
ax[0].set_ylabel('y (million km)')

plt.gca().set_aspect('equal', adjustable='box')

# def update(frame):
#     scatter.set_offsets(simulation[frame*SIM_SPEED]*scale)
#     return scatter,
# anim = animation.FuncAnimation(fig, update, frames=range(SIM_LEN//SIM_SPEED), interval=50, blit=True)

plt.show()
plt.close()