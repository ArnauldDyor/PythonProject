from tkinter import *

from Map.Bloc import Bloc


class Pillier(Bloc):

    def draw(self):

        self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill='grey', outline='grey', tag='pillier')