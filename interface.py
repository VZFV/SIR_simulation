import tkinter
from engine import Engine

CANVAS_SIZE = 800
POPULATION = 500


class Interface:
    def __init__(self):
        self.root = tkinter.Tk()
        self.engine = Engine(CANVAS_SIZE, POPULATION)
        self.create_widgets()

    def create_widgets(self):
        frame = tkinter.Frame(self.root)
        strvar = tkinter.StringVar(frame)
        strvar.set(500)
        label = tkinter.Label(frame, text="Population")
        entry = tkinter.Entry(frame, textvariable=strvar)
        label.pack(side=tkinter.LEFT)
        entry.pack(side=tkinter.LEFT)
        frame.pack()
        self.strvar = strvar
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
        self.stats = {"susceptible": 0}
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
        self.root.after(30, self.next_frame)

    def start(self):
        self.engine.create()
        self.engine.infect(10)
        self.root.after(30, self.next_frame)
        self.root.mainloop()

    def restart(self):
        population = int(self.strvar.get())
        self.engine.create(population=population)
        self.engine.infect(10)


if __name__ == "__main__":
    interface = Interface()
    interface.start()
