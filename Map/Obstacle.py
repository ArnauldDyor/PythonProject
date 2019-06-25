from Map.Bloc import Bloc


class Obstacle(Bloc):

    def __init__(self, x0, y0, x1, y1, canvas):
        super().__init__(x0, y0, x1, y1, canvas)

        self.active = True
        self.item = self.canvas.create_rectangle(self.x0, self.y0, self.x1, self.y1, fill='#8c3f37', outline='white', tag='obstacle')

    def delete(self):
        self.active = False
        self.canvas.delete(self.item)