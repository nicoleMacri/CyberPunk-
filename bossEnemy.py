import pygame
from enemy import Enemy

class BossEnemy(Enemy):
    """
    Κλάση για τον υπερεχθρό.
    Προς το παρόν, κληρονομεί απλά από την κλάση Enemy χωρίς επιπλέον λειτουργικότητα.
    Η επιπλέον λειτουργικότητα θα προστεθεί αργότερα.
    """
    def __init__(self, x, y, bullets_group=None, player_object=None, image_path=None):
        super().__init__(x=x, y=y, width=50, height=50, color=(255, 0, 255), speed=2.0, move=None, fin_y=y, hp=50,
                         row=None, col=None, bullets_group=bullets_group, shoot_delay=2000, player_object=player_object, image_path = image_path)

        
        self.image = pygame.image.load(image_path).convert_alpha() # Φόρτωση εικόνας με διαφάνεια

        w = int(self.image.get_width() * 5)  # Κλιμάκωση πλάτους
        h = int(self.image.get_height() * 5)  # Κλιμάκωση ύψους
        self.image = pygame.transform.scale(self.image, (w, h))  # Κλιμάκωση εικόνας
        
        self.follow_speed = 0.05  # Ταχύτητα με την οποία ο υπερεχθρός ακολουθεί τον παίκτη
        self.max_ai_speed = 4.0  # Μέγιστη ταχύτητα κίνησης του υπερεχθρού

    def move_ai(self):
        # πρεπει να εμπλουτιστει και να βελτιωθει
        if not self.player or not self.alive:
            return

        boss_x = self.rect.centerx
        player_x = self.player.rect.centerx

        dx = player_x - boss_x
        velocity_x = dx * self.follow_speed
        velocity_x = max(-self.max_ai_speed, min(self.max_ai_speed, velocity_x))  # Περιορισμός της ταχύτητας

        self.rect.x += velocity_x
        self.x = self.rect.x
    
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        