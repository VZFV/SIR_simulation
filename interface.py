import tkinter
from engine import Engine
from plot import Plot
import multiprocessing

CANVAS_SIZE = 800
POPULATION = 500


class Interface:
    def __init__(self):
        self.root = tkinter.Tk()
        self.env_variables = {
            "population": 500,
            "move_range": 100,
            "large_range_percent": 0.05
        }
        self.strvars = {}
        self.engine = Engine(CANVAS_SIZE, POPULATION)
        self.data_queue = multiprocessing.Queue()
        self.plot = Plot(self.data_queue)
        self.create_widgets()

    def create_widgets(self):
        for var in self.env_variables:
            frame = tkinter.Frame(self.root)
            strvar = tkinter.StringVar(frame)
            strvar.set(self.env_variables[var])
            label = tkinter.Label(frame, text=var, width=20)
            entry = tkinter.Entry(frame, textvariable=strvar)
            label.pack(side=tkinter.LEFT)
            entry.pack(side=tkinter.LEFT)
            frame.pack()
            self.strvars[var] = strvar
        self.canvas = tkinter.Canvas(self.root, height=CANVAS_SIZE, width=CANVAS_SIZE, bg="white")
        self.canvas.pack()
        self.restart_button = tkinter.Button(self.root, text="restart", command=self.restart)
        self.restart_button.pack()

    def draw_people(self):
        color = {
            "susceptible": "green",
            "infectious": "red",
            "recovered": "yellow"
        }
        for person in self.engine.people:
            self.canvas.create_rectangle(person.x - 2, person.y - 2, person.x + 2, person.y + 2,
                                         fill=color[person.status], outline=color[person.status])

    def draw_stats(self):
        self.stats = {}
        for person in self.engine.people:
            self.stats[person.status] = self.stats.get(person.status, 0) + 1
        y_coord = 20
        for stat in self.stats:
            self.canvas.create_text(50, y_coord, text=f"{stat}: {self.stats[stat]}")
            y_coord += 20

    def next_frame(self):
        self.engine.next_frame()
        self.canvas.delete("all")
        self.draw_people()
        self.draw_stats()
        self.data_queue.put({"type": "data", "data": self.stats.get("infectious", 0)})
        self.root.after(30, self.next_frame)

    def start(self):
        self.engine.create(self.env_variables)
        self.engine.infect(10)
        self.root.after(30, self.next_frame)
        self.plot.start()
        self.root.mainloop()

    def restart(self):
        for key in self.env_variables:
            val_type = type(self.env_variables[key])
            self.env_variables[key] = val_type(self.strvars[key].get())
        self.engine.create(self.env_variables)
        self.engine.infect(10)
        self.data_queue.put({"type": "clear"})


if __name__ == "__main__":
    interface = Interface()
    interface.start()
