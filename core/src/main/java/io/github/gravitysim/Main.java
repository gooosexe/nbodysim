package io.github.gravitysim;

import com.badlogic.gdx.ApplicationAdapter;
import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Input;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.OrthographicCamera;
import com.badlogic.gdx.graphics.g2d.BitmapFont;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.graphics.glutils.ShapeRenderer;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.utils.viewport.ScreenViewport;

import java.io.IOException;
import java.text.DecimalFormat;

/** {@link com.badlogic.gdx.ApplicationListener} implementation shared by all platforms. */
public class Main extends ApplicationAdapter {
    private SpriteBatch batch;
    private Simulation simulation;
    private ShapeRenderer shapeRenderer;
    private BitmapFont font;
    private OrthographicCamera camera;
    private ScreenViewport viewport;
    private final DecimalFormat df2 = new DecimalFormat("#.##");
    private final DecimalFormat df5 = new DecimalFormat("#.#####");
    private boolean keyPressed = false;

    float delta;
    int frames;
    double timeElapsed;

    @Override
    public void create() {
        camera = new OrthographicCamera(800, 600);
        camera.setToOrtho(false, 800, 600);
        camera.position.set(0, 0, 0);
        camera.update();

        viewport = new ScreenViewport(camera);

        try {
            simulation = new Simulation("data.json");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        shapeRenderer = new ShapeRenderer();
        batch = new SpriteBatch();
        font = new BitmapFont();
        frames = 0;
    }

    @Override
    public void render() {
        delta = Gdx.graphics.getDeltaTime();
        if (delta > 0.16) {
            delta = 0.16f;
        }
        ScreenUtils.clear(0.15f, 0.15f, 0.2f, 1f);
        keyPressed = false;
        handleInputs();
        camera.update();
        viewport.apply();
        simulation.update(delta);
        shapeRenderer.setProjectionMatrix(camera.combined);
        shapeRenderer.begin(ShapeRenderer.ShapeType.Filled);

        simulation.renderTrails(shapeRenderer, camera);
        simulation.renderBodies(shapeRenderer, camera);
        shapeRenderer.line(
            10, camera.position.y + camera.viewportHeight - 60,
            110, camera.position.y + camera.viewportHeight -60);
        shapeRenderer.end();

        batch.setProjectionMatrix(camera.combined);
        batch.begin();
        font.setColor(1.0f, 1.0f, 1.0f, 1.0f);
        simulation.renderText(batch, font, camera);
        font.draw(batch, "FPS: " + Gdx.graphics.getFramesPerSecond(),
            camera.position.x - camera.viewportWidth/2 + 10,
            camera.position.y - camera.viewportHeight/2 + 20);
        font.draw(batch, "Delta: " + df5.format(delta) + "s",
            camera.position.x - camera.viewportWidth/2 + 10,
            camera.position.y - camera.viewportHeight/2 + 40);
        font.draw(batch, "Time Elapsed: " + df2.format(timeElapsed / 31536000)  + " y",
            camera.position.x - camera.viewportWidth/2 + 10,
            camera.position.y - camera.viewportHeight/2 + 60);
        batch.end();
        frames++;
        timeElapsed += delta * simulation.timestep;
    }

    @Override
    public void resize(int width, int height) {
        viewport.update(width, height);
    }

    @Override
    public void dispose() {
        shapeRenderer.dispose();
        batch.dispose();
    }

    public void handleInputs() {
        if (Gdx.input.isKeyPressed(Input.Keys.R)) simulation.report();
        if (Gdx.input.isKeyPressed(Input.Keys.DOWN)) simulation.timestep *= 0.99;
        if (Gdx.input.isKeyPressed(Input.Keys.UP)) simulation.timestep *= 1.01;
        if (Gdx.input.isKeyPressed(Input.Keys.RIGHT)) simulation.scale *= 1.01;
        if (Gdx.input.isKeyPressed(Input.Keys.LEFT)) simulation.scale *= 0.99;
        if (Gdx.input.isKeyPressed(Input.Keys.W)) camera.translate(0, 1);
        if (Gdx.input.isKeyPressed(Input.Keys.A)) camera.translate(-1, 0);
        if (Gdx.input.isKeyPressed(Input.Keys.S)) camera.translate(0, -1);
        if (Gdx.input.isKeyPressed(Input.Keys.D)) camera.translate(1, 0);
    }
}
