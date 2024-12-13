import math
import turtle
import time

class Planet:
    def __init__(self, name, mass, size, x, y, x_vel, y_vel, color):
        self.name = name
        self.mass = mass
        self.size = size
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.turtle = None

    def move(self, x_new, y_new):
        self.x = x_new
        self.y = y_new
        self.update_turtle()

    def get_position(self):
        return self.x, self.y

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_turtle()

    def get_velocity(self):
        return self.x_vel, self.y_vel

    def set_velocity(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def calculate_distance_from_sun(self, sun):
        dx = sun.x - self.x
        dy = sun.y - self.y
        return math.sqrt(dx**2 + dy**2)

    def create_turtle(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color(self.color)
        self.turtle.penup()
        self.update_turtle()

    def update_turtle(self):
        if self.turtle:
            scale = 250 / 1.496e11
            self.turtle.goto(self.x * scale, self.y * scale)


class Sun:
    def __init__(self, name, mass, size):
        self.name = name
        self.mass = mass
        self.size = size
        self.x = 0.0
        self.y = 0.0
        self.turtle = None

    def get_mass(self):
        return self.mass

    def get_position(self):
        return self.x, self.y

    def create_turtle(self):
        self.turtle = turtle.Turtle()
        self.turtle.shape("circle")
        self.turtle.color("yellow")
        self.turtle.shapesize(self.size / 1e6)
        self.turtle.penup()
        self.turtle.goto(self.x, self.y)


class SolarSystem:
    def __init__(self):
        self.the_sun = None
        self.planets = []

    def add_sun(self, sun):
        self.the_sun = sun

    def add_planet(self, planet):
        self.planets.append(planet)

    def move_planets(self):
        dt = 10000
        for planet in self.planets:

            planet.move(
                planet.x + dt * planet.x_vel,
                planet.y + dt * planet.y_vel
            )

            dist_x = self.the_sun.x - planet.x
            dist_y = self.the_sun.y - planet.y
            distance = math.sqrt(dist_x ** 2 + dist_y ** 2)

            acc_x = (6.67430e-11 * self.the_sun.mass * dist_x) / (distance ** 3)
            acc_y = (6.67430e-11 * self.the_sun.mass * dist_y) / (distance ** 3)
            planet.x_vel += dt * acc_x
            planet.y_vel += dt * acc_y

            #DEBUG
            print(f"{planet.name} Position: {planet.get_position()} Velocity: {planet.get_velocity()}")

    def initialize_turtles(self):
        self.the_sun.create_turtle()
        for planet in self.planets:
            planet.create_turtle()


class Simulation:
    def __init__(self, solar_system, window_width, window_height, duration):
        self.solar_system = solar_system
        self.window_width = window_width
        self.window_height = window_height
        self.duration = duration
        self.screen = turtle.Screen()

    def run(self):
        self.screen.setup(self.window_width, self.window_height)
        self.screen.bgcolor("black")
        self.screen.title("Solar System Simulation")
        self.solar_system.initialize_turtles()

        self.screen.listen()
        self.screen.onkey(self.show_easter_egg, "p")

        running = True

        def exit_simulation():
            nonlocal running
            running = False

        self.screen.onkey(exit_simulation, "q")

        steps = int(self.duration / 0.01)
        while running and steps > 0:
            try:
                self.solar_system.move_planets()
                time.sleep(0.01)
                steps -= 1
            except turtle.Terminator:
                break

        self.screen.bye()

    def show_easter_egg(self):

        if self.solar_system.the_sun.turtle:
            self.solar_system.the_sun.turtle.hideturtle()
        for planet in self.solar_system.planets:
            if planet.turtle:
                planet.turtle.hideturtle()

        temp_turtle = turtle.Turtle()
        temp_turtle.hideturtle()
        temp_turtle.penup()

        self.screen.bgcolor("purple")
        temp_turtle.color("white")
        temp_turtle.goto(0, 0)
        temp_turtle.write("Thank you for a great semester! 🚀",
                          align="center", font=("Arial", 24, "bold"))

        time.sleep(5)

        temp_turtle.clear()
        temp_turtle.hideturtle()
        self.screen.bgcolor("black")

        if self.solar_system.the_sun.turtle:
            self.solar_system.the_sun.turtle.showturtle()
        for planet in self.solar_system.planets:
            if planet.turtle:
                planet.turtle.showturtle()


if __name__ == "__main__":

    solar_system = SolarSystem()

    the_sun = Sun("Sol", 1.989e30, 1.391e6)
    solar_system.add_sun(the_sun)

    earth = Planet("Earth", 5.972e24, 6371, 1.496e11, 0, 0, 29783, "blue")
    mars = Planet("Mars", 6.39e23, 3389, 2.279e11, 0, 0, 24077, "red")

    solar_system.add_planet(earth)
    solar_system.add_planet(mars)

    simulation = Simulation(solar_system, 800, 600, 10)
    simulation.run()
