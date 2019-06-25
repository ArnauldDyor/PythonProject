from Map.Bloc import Bloc
from time import sleep
from threading import *


class Bombe(Bloc):

    def __init__(self, x0, y0, x1, y1, canvas, direction, map):
        super().__init__(x0, y0, x1, y1, canvas)

        self.direction = direction
        self.map = map
        self.item = canvas.create_oval(self.x0, self.y0, self.x1, self.y1, fill="red", outline="red", tag="bomb")
        self.thread = Thread(target=self.anime)
        self.thread.start()


    def alter_color(self, color):
        if color == 'Y':
            self.canvas.itemconfig(self.item, fill="yellow", outline="yellow")
        elif color == 'R':
            self.canvas.itemconfig(self.item, fill="#d31c1c", outline="#d31c1c")
        else:
            return

    def anime(self):

        for i in range(15):
            if i % 2 == 0:
                self.canvas.itemconfig(self.item, fill="#d31c1c", outline="#d31c1c")
            else:
                self.canvas.itemconfig(self.item, fill="yellow", outline="yellow")

            sleep(1 / 15)

        if self.direction == 'D':
            self.canvas.coords(self.item, self.x0 - 15, self.y0 - 20, self.x1 + 30, self.y1 + 25)
        elif self.direction == 'B':
            self.canvas.coords(self.item, self.x0 - 30, self.y0 - 15, self.x1 + 30, self.y1 + 30)
        elif self.direction == 'G':
            self.canvas.coords(self.item, self.x0 - 30, self.y0 - 15, self.x1 + 15, self.y1 + 25)
        elif self.direction == 'H':
            self.canvas.coords(self.item, self.x0 - 30, self.y0 + 35, self.x1 + 30, self.y1 - 50)

        self.canvas.itemconfig(self.item, fill="black", outline="black")
        sleep(1 / 20)

        t = Thread(target=self.check_collision)
        t.start()
        t.join()
        self.canvas.delete(self.item)

    def check_collision(self):

        i = 0
        while i < len(self.map.players):

            if self.map.players[i].alive:

                if self.map.players[i].isExplosed():
                    self.map.players[i].dead()

            i += 1

        j = 0
        while j < len(self.map.obstacles):

            if self.map.obstacles[i].active:

                if self.map.obstacles[j].isExplosed():
                    self.map.obstacles[j].delete()
            j += 1
