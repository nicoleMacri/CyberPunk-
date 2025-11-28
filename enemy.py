import pygame
from entities import Entities
from bullet import Bullet

class Enemy(Entities):
    #alive = True
    def __init__(self, x, y, width, height, color, speed, direction, row = None, col = None,
                 bullets_group=None, shoot_delay = 1500, row_height=None,
                 hp = 10, *groups):
        """
        bullets_group: Προαιρετική ομάδα sprite για τις σφαίρες που θα πυροβολεί ο εχθρός.
        shoot_delay: Χρόνος καθυστέρησης μεταξύ των πυροβολισμών σε milliseconds. (2000 ms = 2 sec)
        *groups: Προαιρετικά, ομάδες sprite στις οποίες θα προστεθεί ο εχθρός.
        """
        # Καλούμε πρώτα τον constructor της υπερκλάσης
        super().__init__(x, y, width, height, color, speed, *groups)

        # Ιδιότητες γαι την θέση του εχθρού στο grid
        self.direction = direction
        self.row = row
        self.col = col

        # Ιδιότητες για τον πυροβολισμό
        self.bullets_group = bullets_group
        self.shoot_delay = int(shoot_delay)
        self.last_shoot_time = pygame.time.get_ticks() - self.shoot_delay  # Χρόνος του τελευταίου πυροβολισμού0

        # Ιδιότητες για health kai alive
        self.hp = int(hp)
        self.alive = True

        
        self.movement_done = False
        self.start_y = self.rect.y
        if row_height is not None: 
            self.target_y = self.start_y + int(row_height * 0.5)
        else: 
            self.target_y = self.start_y + (self.rect.height // 2)

    def activate(self, row_height=None):
        self.movement_done = False
        self.start_y = self.rect.y
        if row_height is not None: 
            self.target_y = self.start_y + int(row_height * 0.5)
        self.alive = True

    def take_damage(self, damage=1):
        if not self.alive:
            return
        
        self.hp -= int(damage)
        if self.hp <= 0:
            self.die()

    def die(self):
        if not self.alive:
            return
        self.alive = False
        self.movement_done = True
        self.kill()

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
        """
        Παίρνει προαιρετικά ως όρισμα την active_row για να αποφασίσει αν θα κινηθεί.
        Αν η active_row είναι None δηλαδή δεν έχει περαστεί, τότε θεωρεί ότι όλοι οι εχθροί πρέπει να κινηθούν.
        Αν η active_row έχει περαστεί, τότε μόνο οι εχθροί της συγκεκριμένης σειράς θα κινηθούν.
        Τέλος, καλεί την update της υπερκλάσης για τυχον επιπλεόν λειτουργικότητα.

        --- Παράδειγγμα κλήσεων ---
        enemies_group.update()  # args=(), kwargs={}, active_row=None -> Όλοι οι εχθροί κινούνται
        enemies_group.update(active_row=2)  # args=(), kwargs={'active_row': 2} -> Μόνο οι εχθροί της σειράς 2 κινούνται
        enemies_group.update(3)  # args=(3,), kwargs={} -> Μόνο οι εχθροί της σειράς 3 κινούνται
        """
        active_row = kwargs.get('active_row', None)
        if active_row is None and args:
            active_row = args[0]

        if not self.alive:
            return
        
        if active_row is None or self.row == active_row:
            if not self.movement_done:
                self.auto_move()
                if self.y >= self.target_y:
                    self.y = self.target_y
                    self.movement_done = True
            
        super().update(*args, **kwargs)

    def shoot(self, bullets_group=None):
        if not self.alive:
            return None
        
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time < self.shoot_delay:
            return None  # Δεν επιτρέπεται ο πυροβολισμός ακόμα


        print(f"[shoot] Enemy ({self.row},{self.col}) at y={self.rect.y} shoots at t={now}")

        
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

   

    