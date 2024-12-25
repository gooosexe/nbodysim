import numpy as np

class Body:
    """A class to represent a celestial body.
    === Instance Attributes ===
    pos: The position of the body in the form of a pygame.Vector2 in meters.
    vel: The velocity of the body in the form of a pygame.Vector2 in meters
    per second.
    acc: The acceleration of the body in the form of a
    pygame.Vector2 in meters per second squared. mass: The mass of the body
    in kilograms. radius: The radius of the body in meters.
    """
    pos: np.array
    vel: np.array
    acc = np.array([0, 0])
    mass: np.float64
    radius: np.float64

    def __init__(self, pos, vel, mass, radius):
        self.pos = pos
        self.vel = vel
        self.mass = mass
        self.radius = radius

    def __str__(self):
        return (f'pos: {self.pos}, vel: {self.vel}, acc: {self.acc}, '
                f'mass: {self.mass}, radius: {self.radius}')

    def update(self, delta, timestep):
        """Updates the position and velocity of the body.
        """
        self.vel += self.acc * delta * timestep
        self.pos += self.vel * delta * timestep

    def render(self):
        """Renders the body on the screen.
        Radius is the base 10 log of the mass.
        Rendered position is the actual position divided by 1 billion.
        Place 0, 0 at the center of the screen.
        """