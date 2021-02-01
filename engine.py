import random
from vector import Vector

MOVE_RANGE = 50
MOVE_SPEED = 3
UNSAFE_DISTANCE = 5
INFECTIOUS_RATE = 0.3
INFECTIOUS_DURATION = 300


class Person:
    def __init__(self, engine):
        self.position = Vector(random.randrange(0, engine.size), random.randrange(0, engine.size))
        self.home = self.position.copy()
        self.move_target = self.home.copy()
        self.move_range = MOVE_RANGE
        self.move_speed = MOVE_SPEED
        self.status = "susceptible"
        self.infectious_dur_left = 0

    @property
    def x(self):
        return self.position.x

    @property
    def y(self):
        return self.position.y

    def get_new_target(self):
        self.move_target = self.home + Vector(
            random.uniform(-self.move_range, self.move_range),
            random.uniform(-self.move_range, self.move_range)
        )
        self.step = (self.move_target - self.position).uniform(self.move_speed)

    def move(self):
        if self.position == self.move_target:
            self.get_new_target()

        if (self.move_target - self.position).length < self.move_speed:
            self.position = self.move_target.copy()
        else:
            self.position = self.position + self.step

    def too_close(self, other):
        return (other.position - self.position).length < UNSAFE_DISTANCE

    def try_infect(self, other):
        if random.uniform(0,1) < INFECTIOUS_RATE:
            other.status = "infectious"
            other.infectious_dur_left = INFECTIOUS_DURATION


class Engine:
    def __init__(self, size, population):
        self.size = size
        self.population = population
        self.people = []

    def create(self, population=None):
        if population:
            self.population = population
        self.people = []
        for i in range(self.population):
            self.people.append(Person(self))

    def next_frame(self):
        for person in self.people:
            person.move()
            if person.status == "infectious":
                for target in self.people:
                    if target.status == "susceptible" and target.too_close(person):
                        person.try_infect(target)
                person.infectious_dur_left -= 1
                if person.infectious_dur_left == 0:
                    person.status = "recovered"

    def infect(self, number):
        initial_infected = random.sample(self.people, number)
        for person in initial_infected:
            person.status = "infectious"
            person.infectious_dur_left = random.randrange(1, INFECTIOUS_DURATION + 1)
