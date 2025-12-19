import pygame
import random
from entities import Entities
from bullet import Bullet


enemy_images = [

    "assets/server_image_blue.png",
    "assets/server_image_green.png",
    "assets/server_image_red.png",
    "assets/server_image_cyan.png",
    "assets/server_image_magenta.png"
]

bullet_images = [
    "assets/zero_bullet.png",
    "assets/one_bullet.png"
]

class Enemy(Entities):
    def __init__(self, x, y, width, height, color, speed,
                move, 
                fin_y,
                row = None, col = None,
                bullets_group=None,
                shoot_delay = 1500,
                row_height=None,
                hp = None,
                player_object=None,
                image_path=None,
                *groups):
        """
        bullets_group: Προαιρετική ομάδα sprite για τις σφαίρες που θα πυροβολεί ο εχθρός.
        shoot_delay: Χρόνος καθυστέρησης μεταξύ των πυροβολισμών σε milliseconds. (2000 ms = 2 sec)
        *groups: Προαιρετικά, ομάδες sprite στις οποίες θα προστεθεί ο εχθρός.
        """
        # Καλούμε πρώτα τον constructor της υπερκλάσης
        super().__init__(x, y, width, height, color, speed, *groups)

        self.player = player_object

        # Ιδιότητες γαι την θέση του εχθρού στο grid
        self.move = move
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
        
        self.target_y = fin_y

        # ----- sprite εχθρού -----
        image_path = random.choice(enemy_images) 
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha() # Φόρτωση εικόνας με διαφάνεια
        else: 
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        w = int(self.image.get_width() * 0.5)  # Κλιμάκωση πλάτους
        h = int(self.image.get_height() * 0.5)  # Κλιμάκωση ύψους
        self.image = pygame.transform.scale(self.image, (w, h))  # Κλιμάκωση εικόνας

        self.rect = self.image.get_rect() 
        self.rect.center =(self.x,self.y) # Κεντράρισμα του rect στην αρχική θέση

    def activate(self, row_height=None):
        """
        Μέθοδος για την ενεργοποίηση του εχθρού.
        """
        self.movement_done = False
        #self.start_y = self.rect.y
        #self.target_y = self.start_y + int(row_height * 0.5) 
        #if row_height is not None: 
        #    self.target_y = self.start_y + int(row_height * 0.5)
        #self.alive = True

    def take_damage(self, damage=1):
        """ Μέθοδος για damage του εχθρού. 
        Μειώνει το hp του εχθρού κατά damage.  Αν το hp φτάσει στο 0 ή κάτω, καλεί τη μέθοδο die() για τον θανάτο του εχθρού.
        """
        if not self.alive:
            return
        
        self.hp -= int(damage)
        if self.hp <= 0:
            self.die()

    def die(self):
        """ Μέθοδος για τον θάνατο του εχθρού. """
        if not self.alive:
            return
        self.alive = False
        self.movement_done = True
        self.kill() # Αφαίρεση του εχθρού από όλα τα groups
        self.player.score_point()  # Κλήση της μεθόδου score_point() του παίκτη

    # Μέθοδος για την αυτοματοποιημένη κίνηση του εχθρού
    def auto_move(self, move=None):   
        if self.movement_done:
            return
        if self.move == "left":
            self.move_left(self.speed)
        elif self.move == "right":
            self.move_right(self.speed)
        elif self.move == "up":
            self.move_up(self.speed)
        elif self.move == "down":
            self.move_down(self.speed)
        
        

    def update(self, *args, **kwargs):
        """
        Μέθοδος για την ενημέρωση της κατάστασης του εχθρού.

        """
        if not self.alive:
            return
        
        if not self.movement_done:
            self.auto_move(move="down")
            if hasattr(self, 'y'):
                if self.y >= self.target_y:
                    self.y = self.target_y
                    self.movement_done = True
            else:
                if self.rect.y >= self.target_y:
                    self.rect.y = self.target_y
                    self.movement_done = True
        
        super().update(*args, **kwargs)

    def shoot(self):
        """
        Μέθοδος για τον πυροβολισμό από τον εχθρό.

        """
        # πρέπει να διορθωθεί γιατι πυροβολει μονο στο κεντρο;;;
        if not self.alive:
            return None
        
        now = pygame.time.get_ticks()
        if now - self.last_shoot_time < self.shoot_delay:
            return None  # Δεν επιτρέπεται ο πυροβολισμός ακόμα


        #print(f"[shoot] Enemy ({self.row},{self.col}) at y={self.rect.y} shoots at t={now}")

        # Δημιουργία νέας σφαίρας που κινείται προς τα κάτω
        #STREAM_LENGTH = 8
        #SPACING = 12
        ##BASE_ALPHA = 50
        #ALPHA_STEP = 25
        #for i in range(STREAM_LENGTH):
            #alpha = max(40, BASE_ALPHA - i * ALPHA_STEP)
        bullet = Bullet.from_shooter(
                shooter=self,
                width=6,
                height=10,
                color=(0, 255, 0),
                speed=5.0,
                vx=0.0,
                vy=1.0,
                use_img=True,
                image_path=bullet_images,
                alpha = 255
            )


            #bullet.y -= i * SPACING
            #bullet.rect.y = bullet.y

        self.bullets_group.add(bullet) # Προσθήκη της σφαίρας στην ομάδα σφαιρών εχθρών
        self.last_shoot_time = now # Ενημέρωση του χρόνου του τελευταίου πυροβολισμού

    