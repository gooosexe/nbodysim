package io.github.gravitysim;

public class Body {
    String name;
    Vector2D pos;
    Vector2D vel;
    Vector2D acc;
    double mass;
    double radius;

    /**
     * Constructs a body with a given position, velocity, acceleration, mass, and radius.
     * @param pos the position of the body
     * @param vel the velocity of the body
     * @param acc the acceleration of the body
     * @param mass the mass of the body
     * @param radius the radius of the body
     */
    public Body(String name, Vector2D pos, Vector2D vel, Vector2D acc, double mass, double radius) {
        this.name = name;
        this.pos = pos;
        this.vel = vel;
        this.acc = acc;
        this.mass = mass;
        this.radius = radius;
    }

    @Override
    public String toString() {
        return this.name + " Body {" +
                "pos=" + pos +
                ", vel=" + vel +
                ", acc=" + acc +
                ", mass=" + mass +
                ", radius=" + radius +
                '}';
    }

    /**
     * Updates the position of the body based on its velocity and acceleration.
     * @param dt the change in time
     */
    public void update(float dt) {
        vel.add(acc.cpy().scl(dt));
        pos.add(vel.cpy().scl(dt));
    }

    public Vector2D getPos() {
        return pos;
    }

    public Vector2D getVel() {
        return vel;
    }
}
