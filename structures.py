import numpy as np

class QuadTree:
    """A class to represent a quadtree.
    === Instance Attributes ===
    boundary: The boundary of the quadtree in the form of a list of 4 integers [x, y, width, height]. 
    capacity: The maximum number of bodies that can be stored in a quadtree node. 
    bodies: A list of bodies in the quadtree node. 
    children: A list of 4 quadtree nodes that are children of the current node.
    """
    boundary: list
    capacity: int
    bodies: list
    children: list

    def __init__(self, boundary, capacity, bodies=None):
        self.boundary = boundary
        self.capacity = capacity
        self.bodies = []
        self.children = []
        if bodies is not None:
            for body in bodies:
                self.insert(body)

    def insert(self, body):
        """Inserts a body into the quadtree. 
        If the number of bodies in the node exceeds the capacity, the node is subdivided into 4 children.
        """
        if len(self.children) > 0:
            index = self.get_index(body)
            # if the body fits in a child node, insert it into that node
            if index != -1:
                self.children[index].insert(body)
                return
        self.bodies.append(body)
        if len(self.bodies) > self.capacity:
            if len(self.children) == 0:
                self.subdivide()
            i = 0
            while i < len(self.bodies):
                index = self.get_index(self.bodies[i])
                if index != -1:
                    self.children[index].insert(self.bodies.pop(i))
                else:
                    i += 1

    def subdivide(self):
        """Subdivides the quadtree into 4 children.
        """
        x, y, width, height = self.boundary
        # lower right, lower left, upper left, upper right
        self.children.append(QuadTree([x + width // 2, y, width // 2, height // 2], self.capacity))
        self.children.append(QuadTree([x, y, width // 2, height // 2], self.capacity))
        self.children.append(QuadTree([x, y + height // 2, width // 2, height // 2], self.capacity))
        self.children.append(QuadTree([x + width // 2, y + height // 2, width // 2, height // 2], self.capacity))

    def get_index(self, body):
        """Returns the index of the child that the body sits in.
        """
        x, y, width, height = self.boundary
        pos = body.pos
        if x + width // 2 > pos[0] >= x:
            if y + height // 2 > pos[1] >= y:
                return 1
            elif y + height > pos[1] >= y + height // 2:
                return 2
        elif x + width > pos[0] >= x + width // 2:
            if y + height // 2 > pos[1] >= y:
                return 0
            elif y + height > pos[1] >= y + height // 2:
                return 3
        return -1
    
    def query(self, boundary, found):
        """Returns a list of bodies that are within the boundary.
        """
        if self.intersects(boundary):
            for body in self.bodies:
                if boundary[0] <= body.pos[0] < boundary[0] + boundary[2] and boundary[1] <= body.pos[1] < boundary[1] + boundary[3]:
                    found.append(body)
            for child in self.children:
                child.query(boundary, found)
        return found
    
    def count(self):
        """Returns the number of boxes in the quadtree.
        """
        if len(self.children) == 0:
            return 1
        else:
            count = 0
            for child in self.children:
                count += child.count()
            return count
    
    def contains(self, body):
        """Returns whether the quadtree node contains the body.
        """
        x, y, width, height = self.boundary
        return x <= body.pos[0] < x + width and y <= body.pos[1] < y + height
    
    def intersects(self, boundary):
        """Returns whether the quadtree node intersects with the boundary.
        """
        x, y, width, height = self.boundary
        return x < boundary[0] + boundary[2] and x + width > boundary[0] and y < boundary[1] + boundary[3] and y + height > boundary[1]
    
    def lines(self):
        """Returns a list of lines that represent the boundaries of the quadtree.
        """
        x, y, width, height = self.boundary
        if len(self.children) == 0:
            lines = []
            lines.append([x, y, x + width, y])
            lines.append([x, y, x, y + height])
            lines.append([x + width, y, x + width, y + height])
            lines.append([x, y + height, x + width, y + height])
            return lines
        else:
            lines = []
            for child in self.children:
                lines.extend(child.lines())
            return lines

    def clear(self):
        """Clears the quadtree.
        """
        self.bodies = []
        self.children = []


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
    acc = np.array([0.0, 0.0])
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

    def density(self):
        """Returns the density of the body.
        """
        return self.mass / (4 / 3 * np.pi * self.radius ** 3)