import pygame
import math
from enemy import Enemy

class BossEnemy(Enemy):
    """
    Κλάση για τον υπερεχθρό.
    Προς το παρόν, κληρονομεί απλά από την κλάση Enemy χωρίς επιπλέον λειτουργικότητα.
    Η επιπλέον λειτουργικότητα θα προστεθεί αργότερα.
    """
    def __init__(self, x, y, bullets_group=None, player_object=None, image_path=None):
        super().__init__(x=x, y=y, width=50, height=50, color=(255, 0, 255), 
                         speed=8.0, move=None, fin_y=y, hp=10,
                         row=None, col=None, bullets_group=bullets_group, shoot_delay=2000, player_object=player_object, image_path = image_path)

        
        self.image = pygame.image.load(image_path).convert_alpha() # Φόρτωση εικόνας με διαφάνεια

        w = int(self.image.get_width() * 5)  # Κλιμάκωση πλάτους
        h = int(self.image.get_height() * 5)  # Κλιμάκωση ύψους
        self.image = pygame.transform.scale(self.image, (w, h))  # Κλιμάκωση εικόνας
        self.rect = self.image.get_rect(center=(self.x,self.y)) # Κεντράρισμα του rect στην αρχική θέση

        self.movement_done = False
        self.pos = pygame.Vector2(self._x, self._y)

    def move_ai(self):
        if not self.player or not self.player.alive:
            return  # Δεν υπάρχει παίκτης ή ο παίκτης δεν είναι ζωντανός
        
       
        base_target = pygame.Vector2(self.player.rect.centerx, self.player.rect.centery - 500)
        time = pygame.time.get_ticks() * 0.005  # Ρυθμός ταλάντωσης
        bounce = math.sin(time) * 100  # Πλάτος ταλάντωσης
        target = pygame.Vector2(base_target.x + bounce, base_target.y)

        lerp_factor = 0.05
        self.pos = self.pos.lerp(target, lerp_factor)

        self.rect.center = (int(self.pos.x), int(self.pos.y))

        #target_x_base = self.player.rect.centerx
        #target_y_base = self.player.rect.centery - 400 

        #time = pygame.time.get_ticks() * 0.002  # Ρυθμός ταλάντωσης
        #bounce = math.sin(time) * 100  # Πλάτος ταλάντωσης

        #target_x = target_x_base + bounce
        #target_y = target_y_base
        
        #dx = target_x - self.x
        #dy = target_y - self.y

        #distance = math.hypot(dx, dy)
        #if distance < 50: 
        #    return  # Αποφυγή υπερβολικής προσέγγισης
        
        # Κανονικοποίηση του διανύσματος κίνησης
        #dx /= distance
        #dy /= distance
        # Κίνηση προς τον παίκτη
        #self.x += dx * self.speed * 0.5  # Πιο αργή κίνηση στον άξονα x
        #self.y += dy * self.speed * 0.5  # Πιο αργή κίνηση στον άξονα y
        

    def update(self, *args, **kwargs):
        if not self.alive:
            return
        self.move_ai()
        self.rect.center = (int(self.x), int(self.y))
        #super().update(*args, **kwargs)
        