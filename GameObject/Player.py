from GameObject.Bombe import Bombe
from Map.Bloc import Bloc

class Player(Bloc):

    def __init__(self, x0, y0, x1, y1, id, canvas, map):
        super().__init__(x0, y0, x1, y1, canvas)

        self.id = id
        self.alive = True
        self.map = map
        self.direction = '\0'
        self.mouvement = 9

        # draw
        if self.id == 0:
            couleur = "#40ee38"
        elif self.id == 1:
            couleur = "#5264c9"
        elif self.id == 2:
            couleur = "#d260dc"
        else:
            couleur = "#eac56f"

        self.avatar = self.canvas.create_oval(self.x0, self.y0, self.x1, self.y1, fill=couleur, outline=couleur,
                                              tag='player')

    def move(self):

        with self.map.locks[self.id]:
            if self.direction == 'D':
                self.canvas.move(self.avatar, 5, 0)
                self.x0 += 5
                self.x1 += 5
            elif self.direction == 'G':
                self.canvas.move(self.avatar, -5, 0)
                self.x0 -= 5
                self.x1 -= 5
            elif self.direction == 'B':
                self.canvas.move(self.avatar, 0, 5)
                self.y0 += 5
                self.y1 += 5
            elif self.direction == 'H':
                self.canvas.move(self.avatar, 0, -5)
                self.y0 -= 5
                self.y1 -= 5
            else:
                return

            if self.mouvement == 0:
                return

            self.map.fenetre.after(20, self.move)
            self.mouvement -= 1

    def launch_bomb(self):

        if self.direction == 'D':
            bloc = Bloc(self.x0 + 50, self.y0 + 10, self.x1 + 30, self.y1 - 10, self.canvas)
            if bloc.isCollision(0):
                return
            bombe = Bombe(self.x0 + 50, self.y0 + 10, self.x1 + 30, self.y1 - 10, self.canvas, self.direction, self.map)
        elif self.direction == 'G':
            bloc = Bloc(self.x0 - 30, self.y0 + 10, self.x1 - 50, self.y1 - 10, self.canvas)
            if bloc.isCollision(0):
                return
            bombe = Bombe(self.x0 - 30, self.y0 + 10, self.x1 - 50, self.y1 - 10, self.canvas, self.direction, self.map)
        elif self.direction == 'B':
            bloc = Bloc(self.x0 + 10, self.y0 + 50, self.x1 - 10, self.y1 + 30, self.canvas)
            if bloc.isCollision(0):
                return
            bombe = Bombe(self.x0 + 10, self.y0 + 50, self.x1 - 10, self.y1 + 30, self.canvas, self.direction, self.map)
        elif self.direction == 'H':
            bloc = Bloc(self.x0 + 10, self.y0 - 30, self.x1 - 10, self.y1 - 50, self.canvas)
            if bloc.isCollision(0):
                return
            bombe = Bombe(self.x0 + 10, self.y0 - 30, self.x1 - 10, self.y1 - 50, self.canvas, self.direction, self.map)
        else:
            return

    def dead(self):
        self.alive = False
        self.canvas.delete(self.avatar)

    def oracle(self, direction):

        bloc = Bloc(self.x0, self.y0, self.x1, self.y1, self.canvas)

        if direction == 'D':
            bloc.x0 += 50
            bloc.x1 += 50
            bloc.y0 += 10
            bloc.y1 -= 10
        elif direction == 'G':
            bloc.x0 -= 50
            bloc.x1 -= 50
        elif direction == 'B':
            bloc.y0 += 50
            bloc.y1 += 50
        elif direction == 'H':
            bloc.y0 -= 50
            bloc.y1 -= 50
        else:
            return -1

        tags = []
        for obj in self.canvas.find_overlapping(bloc.x0, bloc.y0, bloc.x1, bloc.y1):

            for tag in self.canvas.gettags(obj):
                tags.append(tag)

        # bordure
        if bloc.x1 > self.map.WIDTH - 50 or bloc.x0 < 50 or bloc.y0 < 50 or bloc.y1 > self.map.HEIGHT - 50:
            tags.append('pillier')

        return tags
