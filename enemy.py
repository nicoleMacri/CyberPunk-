import pygame
from entities import Entities
from bullet import Bullet

class Enemy(Entities):
    #alive = True
    def __init__(self, x, y, width, height, color, speed, direction, row = None, col = None,
                 bullets_group=None, shoot_delay = 1500, *groups):
        """
        bullets_group: Προαιρετική ομάδα sprite για τις σφαίρες που θα πυροβολεί ο εχθρός.
        shoot_delay: Χρόνος καθυστέρησης μεταξύ των πυροβολισμών σε milliseconds. (2000 ms = 2 sec)
        *groups: Προαιρετικά, ομάδες sprite στις οποίες θα προστεθεί ο εχθρός.
        """
        # Καλούμε πρώτα τον constructor της υπερκλάσης
        super().__init__(x, y, width, height, color, speed, *groups)

        # Ορισμός επιπλέον ιδιοτήτων για τον εχθρό
        self.direction = direction
        self.row = row
        self.col = col

        # Ιδιότητες για τον πυροβολισμό
        self.bullets_group = bullets_group
        self.shoot_delay = int(shoot_delay)
        self.last_shoot_time = 0  # Χρόνος του τελευταίου πυροβολισμού

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

    def shoot(self, bullets_group=None):
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time < self.shoot_delay:
            return None  # Δεν επιτρέπεται ο πυροβολισμός ακόμα

        bullet = Bullet.from_shooter(
            self,
            width=4,
            height=10,
            color=(0, 255, 0),
            speed=5.0,
            vx=0.0,
            vy=1.0
        )

        target_group = bullets_group if bullets_group is not None else self.bullets_group
        if target_group is not None:
            target_group.add(bullet)
        
        self.last_shoot_time = now
        return bullet

   

    