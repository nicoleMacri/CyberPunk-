
from entities import Entities

class Enemy(Entities):
    #alive = True
    def __init__(self, x, y, width, height, color, speed, direction):
        self.direction = direction
        super().__init__(x, y, width, height, color, speed)

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

        
   

    