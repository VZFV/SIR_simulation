import multiprocessing


class Plot(multiprocessing.Process):
    def __init__(self, data_queue):
        super().__init__(daemon=True)
        self.data = []
        self.data_queue = data_queue

    def update(self, frame):
        while not self.data_queue.empty():
            element = self.data_queue.get()
            if element["type"] == "clear":
                self.data = []
            elif element["type"] == "data":
                self.data.append(element["data"])
        y = self.data
        x = [i for i in range(len(self.data))]
        self.ax.relim()
        self.ax.autoscale_view()
        self.line.set_data(x, y)
        return self.line,

    def animate_init(self):
        self.line.set_data([], [])
        return self.line,

    def run(self):
        import matplotlib.pyplot as plt
        from matplotlib import animation
        self.fig = plt.figure()
        self.ax = plt.axes()
        self.line, = self.ax.plot([1, 2, 3], [1, 2, 4])
        _ = animation.FuncAnimation(self.fig,
                                    self.update,
                                    init_func=self.animate_init,
                                    frames=range(1, 100),
                                    interval=100,
                                    blit=False)

        plt.show()


if __name__ == "__main__":
    p = Plot()
    p.start()
