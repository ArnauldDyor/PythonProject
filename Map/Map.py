from threading import Thread, RLock, enumerate
from tkinter import *
from random import randint
from IA.IAVictor import IAVictor
from Map.ChoiceIA import ChoiceIA
from Map.Pillier import Pillier
from Map.Obstacle import Obstacle
from GameObject.Player import Player


class Map:

    def __init__(self):

        # taille de la map
        self.WIDTH = 1050
        self.HEIGHT = 550

        # liste joueur
        self.players = []
        self.IAs = []

        # arriere plan
        self.fenetre = Tk()
        self.fenetre.title("PROJET PYTHON")
        self.fenetre.config(background='#00997b')
        self.champ_label = Label(self.fenetre, text=">>>>>   BOMBERMAN    <<<<<", bg='#00997b', height=3, font='Arial 30 bold')
        self.champ_label.pack()
        self.canevas = Canvas(self.fenetre, width=self.WIDTH, height=self.HEIGHT, bg="white")
        self.canevas.pack()

        # boutons

        self.buttons = Canvas(self.fenetre, width=self.WIDTH, height=self.HEIGHT)
        self.player_buton = Button(self.buttons, text="Add player", width=30, height=5, bg="white",
                                   command=self.add_player)
        self.player_buton.pack(side=LEFT)
        self.start = Button(self.buttons, text="Start", width=30, height=5, bg="white", command=self.start)
        self.start.pack(side=LEFT)
        self.exit = Button(self.buttons, text="Exit", width=30, height=5, bg="white", command=self.fenetre.destroy)
        self.exit.pack(side=LEFT)

        self.buttons.pack(side=TOP)

        # initialisation carte
        self.obstacles = []
        self.pilliers = []
        self.create_pillier()
        self.create_obstacle()
        self.create_bordure()

        # locks pour les threads des players
        self.locks = []

    def create_pillier(self):

        for i in range(4):
            for j in range(9):
                pillier = Pillier(100 + 100 * j, 100 + 100 * i, 150 + 100 * j, 150 + 100 * i, self.canevas)
                pillier.draw()
                self.pilliers.append(pillier)

    def create_bordure(self):

        # floor
        self.canevas.create_rectangle(0, 0, self.WIDTH, 50, fill='grey', outline='grey')
        self.canevas.create_rectangle(0, self.HEIGHT - 50, self.WIDTH, self.HEIGHT, fill='grey', outline='grey')

        # wall
        self.canevas.create_rectangle(0, 0, 50, self.HEIGHT, fill='grey', outline='grey')
        self.canevas.create_rectangle(self.WIDTH - 50, 0, self.WIDTH, self.HEIGHT, fill='grey', outline='grey')

    def create_obstacle(self):

        for i in range(5):
            for j in range(15):

                if randint(0, 5) < 1:
                    continue

                else:
                    obs = Obstacle(151 + 50 * j, 151 + 50 * i, 199 + 50 * j, 199 + 50 * i, self.canevas)
                    if obs.isCollision(1):
                        self.canevas.delete(obs.item)

        # floor
        width = 200
        while width < self.WIDTH - 200:
            obs = Obstacle(width, 51, width + 50, 99, self.canevas)
            if obs.isCollision(1):
                self.canevas.delete(obs.item)
            self.obstacles.append(obs)

            obs = Obstacle(width, 451, width + 50, 499, self.canevas)
            if obs.isCollision(1):
                self.canevas.delete(obs.item)
            self.obstacles.append(obs)
            width += 50

        # wall
        height = 150
        while height < self.HEIGHT - 150:
            obs = Obstacle(51, height, 99, height + 50, self.canevas)
            if obs.isCollision(1):
                self.canevas.delete(obs.item)
            self.obstacles.append(obs)

            obs = Obstacle(951, height, 999, height + 50, self.canevas)
            if obs.isCollision(1):
                self.canevas.delete(obs.item)
            self.obstacles.append(obs)
            height += 50

    def add_player(self):

        if len(self.players) > 3:
            return

        # choix de l'IA
        choice = ChoiceIA()
        choice = choice.getIA()
        if choice == -1:
            return
        else:
            self.IAs.append(choice)

        if len(self.players) == 0:
            joueur = Player(55, 55, 95, 95, 0, self.canevas, self)
        elif len(self.players) == 1:
            joueur = Player(955, 55, 995, 95, 1, self.canevas, self)
        elif len(self.players) == 2:
            joueur = Player(55, 455, 95, 495, 2, self.canevas, self)
        elif len(self.players) == 3:
            joueur = Player(955, 455, 995, 495, 3, self.canevas, self)
        else:
            return

        self.players.append(joueur)

    def move_player(self, index, direction):

        # test si déplacement est possible
        if direction == 'D':
            colision = self.canevas.find_overlapping(self.players[index].x0 + 5, self.players[index].y0,
                                                     self.players[index].x1 + 5, self.players[index].y1)
        elif direction == 'G':
            colision = self.canevas.find_overlapping(self.players[index].x0 - 5, self.players[index].y0,
                                                     self.players[index].x1 - 5, self.players[index].y1)
        elif direction == 'B':
            colision = self.canevas.find_overlapping(self.players[index].x0, self.players[index].y0 + 5,
                                                     self.players[index].x1, self.players[index].y1 + 5)
        elif direction == 'H':
            colision = self.canevas.find_overlapping(self.players[index].x0, self.players[index].y0 - 5,
                                                     self.players[index].x1, self.players[index].y1 - 5)
        else:
            return

        if len(colision) > 1:
            return
        else:
            self.players[index].direction = direction
            self.players[index].mouvement = 9

            thread = Thread(target=self.players[index].move)
            thread.start()

    def start(self):

        if len(self.IAs) < 1 or len(self.players) < 2:
            return

        ias = []

        for i in range(0, len(self.players)):

            if self.IAs[i] == 0:
                ias.append(IAVictor())
            else:
                ias.append(IAVictor())

            self.locks.append(RLock())

        self.play(ias)



    def play(self, ias):

        for i in range(0, len(self.players)):

            if not self.players[i].alive:
                continue

            mv = ias[i].control(self.players[i])

            # déplacement
            if mv[0] == 'D':
                self.move_player(i, mv[1])
            # si bombe
            else:
                self.players[i].direction = mv[1]
                self.players[i].launch_bomb()

        # self.parti(ias)
