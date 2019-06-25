from random import randint


# RECOIT UN OBJET "PLAYER" ET DOIT RETOURNER UN TUPLE ACTION + DIRECTION
# ACTION : 'D' pour déplacement, 'B' pour bombe
# DIRECTION : 'G', 'D', 'H', 'B'

class IAVictor:

    def __init__(self):
        self.directions = ['G', 'D', 'B', 'H']
        self.objets = []

    def control(self, player):

        self.analyse_objets(player)

        # si bombe on se casse
        if len(self.get_bomb()) > 0 and len(self.get_empty()) > 0:
            return 'D', self.get_empty()[0]
        #si pas de bombe on pose
        elif len(self.get_bomb()) == 0:
            dest = []
            i = 0
            while i < len(self.objets):
                if self.objets[i] == 'empty':
                    dest.append(self.directions[i])
                i += 1

            return 'B', dest[randint(0, len(dest) - 1)]
        elif len(self.get_empty()) > 0:
            return self.get_empty()[0]
        else:
            return 'D', 'D'

    def analyse_objets(self, player):

        for dir in self.directions:
            if len(player.oracle(dir)) < 1:
                self.objets.append('empty')
            else:
                self.objets.append(player.oracle(dir)[0])

    def get_empty(self):

        dest = []
        i = 0
        while i < len(self.objets):
            if self.objets[i] == 'empty':
                dest.append(self.directions[i])
            i += 1

        return dest

    def get_bomb(self):

        dest = []
        i = 0
        while i < len(self.objets):
            if self.objets[i] == 'bomb':
                dest.append(self.directions[i])
            i += 1

        return dest
