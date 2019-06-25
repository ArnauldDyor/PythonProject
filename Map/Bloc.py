class Bloc:

    def __init__(self, x0, y0, x1, y1, canvas):

        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.canvas = canvas

    def getPosition(self):
        return (self.x0, self.y0, self.x1, self.y1)

    def isCollision(self, strat):

        if len(self.canvas.find_overlapping(self.x0, self.y0, self.x1, self.y1)) > strat:
            return True

        return False

    def isExplosed(self):

        for obj in self.canvas.find_overlapping(self.x0, self.y0, self.x1, self.y1):

            if len(self.canvas.gettags(obj)) > 0:
                if self.canvas.gettags(obj)[0] == 'bomb':

                    return True

        return False
