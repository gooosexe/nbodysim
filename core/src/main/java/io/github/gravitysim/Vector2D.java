package io.github.gravitysim;

public class Vector2D {
    public double x;
    public double y;

    public Vector2D(double x, double y) {
        this.x = x;
        this.y = y;
    }

    @Override
    public String toString() {
        return "[" + x + ", " + y + ']';
    }

    public void add(Vector2D other) {
        this.x = this.x + other.x;
        this.y = this.y + other.y;
    }

    public void sub(Vector2D other) {
        this.x = this.x - other.x;
        this.y = this.y - other.y;
    }

    public Vector2D scl(double scalar) {
        this.x = this.x * scalar;
        this.y = this.y * scalar;
        return this;
    }

    public Vector2D cpy() {
        return new Vector2D(this.x, this.y);
    }

    public double len() {
        return Math.sqrt(this.x * this.x + this.y * this.y);
    }

    public Vector2D nor() {
        double len = len();
        if (len != 0) {
            return new Vector2D(this.x / len, this.y / len);
        }
        return new Vector2D(0, 0);
    }

    public double dot(Vector2D other) {
        return this.x * other.x + this.y * other.y;
    }

    public Vector2D rotate(double degrees) {
        double rad = Math.toRadians(degrees);
        double cos = Math.cos(rad);
        double sin = Math.sin(rad);
        return new Vector2D(this.x * cos - this.y * sin, this.x * sin + this.y * cos);
    }

    public double angle(Vector2D other) {
        return Math.toDegrees(Math.atan2(other.y, other.x) - Math.atan2(this.y, this.x));
    }

    public void set(double x, double y) {
        this.x = x;
        this.y = y;
    }

    public Vector2D set(Vector2D other) {
        this.x = other.x;
        this.y = other.y;
        return this;
    }
}
