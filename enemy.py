
from entities import Entities

class Enemy(Entities):
    #alive = True
    def __init__(self, x, y, width, height, color, speed, direction, row = None, col = None, *groups):
        # Καλούμε πρώτα τον constructor της υπερκλάσης
        super().__init__(x, y, width, height, color, speed, *groups)

        # Ορισμός επιπλέον ιδιοτήτων για τον εχθρό
        self.direction = direction
        self.row = row
        self.col = col

    # Μέθοδος για την αυτοματοποιημένη κίνηση του εχθρού
    def auto_move(self):   
        if self.direction == "left":
            self.move_left(self.speed)
        elif self.direction == "right":
            self.move_right(self.speed)
        elif self.direction == "up":
            self.move_up(self.speed)
        elif self.direction == "down":
            self.move_down(self.speed)
        #Περιορισμός του ορθογωνίου να μην βγαίνει εκτός οθόνης

    def update(self, *args, **kwargs):
        last_row = kwargs.get('last_row', None)
        if last_row is None and args:
            last_row = args[0]
        if last_row is None or self.row == last_row:
            self.auto_move()
            
        super().update(*args, **kwargs)


   

    