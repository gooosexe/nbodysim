package io.github.gravitysim;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.LinkedList;

import com.badlogic.gdx.math.Vector2;
import com.badlogic.gdx.math.Vector3;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.JsonNode;

// TODO: add collision method

/**
 * A class that represents a simulation of a system of bodies. Contains a list of bodies and valuable constants.
 */
public class Simulation {
    double timestep;
    double scale;
    String name;
    final double G = 6.67430e-11f;
    final double AU = 1.496e11f;
    final double LY = 9.461e15f;
    final double PC = 3.086e16f;
    ArrayList<Body> bodies;
    ArrayList<LinkedList<Vector2D>> trails;

    /**
     * Constructs a simulation with a given timestep, scale, and list of bodies.
     * @param filePath the path to the file containing the bodies
     */
    public Simulation(String filePath) throws IOException {
        ObjectMapper objectMapper = new ObjectMapper();
        File file = Gdx.files.internal(filePath).file();

        JsonNode fullData = objectMapper.readTree(file);
        JsonNode bodiesData = fullData.get("bodies");

        this.name = fullData.get("name").asText();
        this.scale = fullData.get("scale").floatValue();
        this.timestep = fullData.get("timestep").floatValue();

        this.bodies = new ArrayList<>();
        trails = new ArrayList<>();

        for (JsonNode bodyData : bodiesData) {
            String name = bodyData.get("name").asText();
            float mass = bodyData.get("mass").floatValue();
            float radius = bodyData.get("radius").floatValue();
            Vector2D bodyPos = new Vector2D(
                bodyData.get("position").get("x").floatValue(),
                bodyData.get("position").get("y").floatValue()
            );
            Vector2D bodyVel = new Vector2D(
                bodyData.get("velocity").get("x").floatValue(),
                bodyData.get("velocity").get("y").floatValue()
            );
            this.addBody(new Body(name, bodyPos, bodyVel, new Vector2D(0, 0), mass, radius));
            trails.add(new LinkedList<>());
        }
        System.out.println(this.name);
        System.out.println(this.scale);
        System.out.println("timestep " + this.timestep);
        for (Body body : bodies) System.out.println(body);
    }

    /**
     * Adds a body to the simulation.
     * @param body the body to add
     */
    public void addBody(Body body) {
        bodies.add(body);
    }

    /**
     * Removes a body from the simulation.
     * @param body the body to remove
     */
    public void removeBody(Body body) {
        bodies.remove(body);
    }

    /**
     * Calculates the gravitational force between two bodies.
     * @param body1 the first body
     * @param body2 the second body
     * @return the force vector acting on the first body
     */
    public Vector2D getForce(Body body1, Body body2) {
        Vector2D displacement = new Vector2D(body2.pos.x - body1.pos.x, body2.pos.y - body1.pos.y);
        double r = displacement.len();
        //System.out.printf("Distance between %s and %s: %f\n", body1.name, body2.name, r);
        //System.out.println(force);
        return displacement.nor().scl((float) (G * (body1.mass * body2.mass) / (Math.pow(r, 2))));
    }

    /**
     * Updates the simulation by calculating the net forces on each body and updating their positions and velocities.
     * @param delta the time since the last update
     */
    public void update(float delta) {
        // Reset acceleration
        for (Body body : bodies) body.acc.set(0, 0);

        // Calculate net forces on each body
        for (int i = 0; i < bodies.size(); i++) {
            Body body1 = bodies.get(i);
            for (int j = 0; j < bodies.size(); j++) {
                if (i == j) continue;
                Body body2 = bodies.get(j);
                Vector2D force = getForce(body1, body2);
                body1.acc.add(force.cpy().scl(1 / body1.mass));
            }
            //System.out.println(body1.name + " " + body1.acc);
        }

        // Update each body
        for (Body body : bodies) body.update((float) (delta * timestep));
    }

    /**
     * Renders the simulation using a ShapeRenderer.
     * @param shapeRenderer the ShapeRenderer to use
     */
    public void renderBodies(ShapeRenderer shapeRenderer, OrthographicCamera camera) {
        shapeRenderer.setColor(1, 1, 1, 1);
        int height = Gdx.graphics.getHeight();
        for (Body body : bodies) {
            float radius = (float) (Math.log(body.radius) / Math.log(50));
            double xpos = body.getPos().x / scale;
            double ypos = body.getPos().y / scale;
            //System.out.println(body.getPos());
            //System.out.printf("%f %f %f\n", body.getPos().x, body.getPos().y, radius);
            //System.out.printf("%f %f %f\n", xpos, ypos, radius);
            shapeRenderer.circle((float) xpos, (float) ypos, radius);
        }
    }

    public void renderText(SpriteBatch batch, BitmapFont font, OrthographicCamera camera) {
        Vector3 cameraPos = camera.position;
        font.draw(batch, "Timescale: " + readableTimestep(),
            cameraPos.x - camera.viewportWidth/2 + 10,
            cameraPos.y + camera.viewportHeight/2 - 10);
        font.draw(batch, "Scale: " + readableScale(),
            cameraPos.x - camera.viewportWidth/2 + 10,
            cameraPos.y + camera.viewportHeight/2 - 30);
        for (Body body : bodies) {
            float radius = (float) (Math.log(body.radius) / Math.log(50));
            double xpos = body.getPos().x / scale;
            double ypos = body.getPos().y / scale;
            //System.out.println(body.getPos());
            //System.out.printf("%f %f %f\n", body.getPos().x, body.getPos().y, radius);
            //System.out.printf("%f %f %f\n", xpos, ypos, radius);
            font.draw(batch, body.name, (float) xpos - 20, (float) ypos + radius + 20);
        }
    }

    public void renderTrails(ShapeRenderer shapeRenderer, OrthographicCamera camera) {
        int MAX_TRAIL_LENGTH = 1000;
        for (int i = 0; i < bodies.size(); i++) {
            if (trails.get(i).size() > MAX_TRAIL_LENGTH) trails.get(i).removeFirst();
            trails.get(i).add(bodies.get(i).pos.cpy());
            for (int j = 0; j < trails.get(i).size() - 1; j++) {
                Vector2D pos1 = trails.get(i).get(j);
                Vector2D pos2 = trails.get(i).get(j + 1);
                float alpha = ((float) j / trails.get(i).size());
                Gdx.gl.glEnable(GL20.GL_BLEND);
                Gdx.gl.glBlendFunc(GL20.GL_SRC_ALPHA, GL20.GL_ONE_MINUS_SRC_ALPHA);
                shapeRenderer.setColor(0.5f, 0.5f, 0.5f, alpha);
                shapeRenderer.rectLine(
                   new Vector2((float) (pos1.x / scale), (float) (pos1.y / scale)),
                    new Vector2((float) (pos2.x / scale), (float) (pos2.y / scale)), 2);
            }
        }
    }

    public String readableScale() {
        return
            (scale >= 94607304725808.0) ? String.format("%.2f astronomical units per 100 pixels", scale / 94607304725808.0) :
            (scale >= 1495978707.0) ? String.format("%.2f AU per 100 pixels", scale / 1495978707.0) :
            (scale >= 179875474.0) ? String.format("%.2f light minute per 100 pixels", scale / 179875474.0) :
            (scale >= 10.0) ? String.format("%.2f kilometers per 100 pixels", scale / 10.0) :
            String.format("%f meters per pixel", scale);
    }

    public String readableTimestep() {
        return
            (timestep >= 31536000.0) ? String.format("%.2f years per second", timestep / 31536000.0) :
            (timestep >= 2628000.0) ? String.format("%.2f months per second", timestep / 2628000.0) :
            (timestep >= 604800.0) ? String.format("%.2f weeks per second", timestep / 604800.0) :
            (timestep >= 86400.0) ? String.format("%.2f days per second", timestep / 86400.0) :
            (timestep >= 3600.0) ? String.format("%.2f hours per second", timestep / 3600.0) :
            (timestep >= 60.0) ? String.format("%.2f minutes per second", timestep / 60.0) :
            String.format("%f seconds per second", timestep);
    }

    /**
     * Logs the data of each body to a csv file.
     */
    public void report() {
        StringBuilder sb = new StringBuilder();
        for (Body body : bodies) {
            sb.append(body.name).append(": ");
            sb.append("pos: ").append(body.pos).append(", ");
            sb.append("vel: ").append(body.vel).append(", ");
            sb.append("acc: ").append(body.acc).append(", ");
            sb.append("mass: ").append(body.mass).append(", ");
            sb.append("radius: ").append(body.radius).append("\n");
        }
        System.out.println(sb.toString());
    }

}
