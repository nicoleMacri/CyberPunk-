import pygame
import math
import random
from enemy import Enemy
from entities import Entities
from bullet import Bullet

bullet_images = [
    "assets/zero_bullet.png",
    "assets/one_bullet.png"
]

class BossEnemy(Entities):
    """
    Κλάση για τον υπερεχθρό.
    Προς το παρόν, κληρονομεί απλά από την κλάση Enemy χωρίς επιπλέον λειτουργικότητα.
    Η επιπλέον λειτουργικότητα θα προστεθεί αργότερα.
    """
    def __init__(self, x, y, width, height, speed, players_group,
                bullets_group,image_path, hp, shooter_delay=800,
                target_switch_delay=200, *groups):
        super().__init__(x, y, width, height, speed, *groups)

        self.hp = hp
        self.alive = True

        self.players_group = players_group
        self.bullets_group = bullets_group

        self.target = None
        self.target_switch_delay = target_switch_delay
        self.last_target_switch_time = pygame.time.get_ticks()

        self.shoot_delay = shooter_delay
        self.last_shoot_time = pygame.time.get_ticks()


        
        self.image = pygame.image.load(image_path).convert_alpha() # Φόρτωση εικόνας με διαφάνεια

        w = int(self.image.get_width() * 5)  # Κλιμάκωση πλάτους
        h = int(self.image.get_height() * 5)  # Κλιμάκωση ύψους
        self.image = pygame.transform.scale(self.image, (w, h))  # Κλιμάκωση εικόνας
        self.rect = self.image.get_rect(center=(self.x,self.y)) # Κεντράρισμα του rect στην αρχική θέση

        self.movement_done = False
        self.pos = pygame.Vector2(self._x, self._y)

    
    def target_player(self):
        now = pygame.time.get_ticks()
        
        
        if now - self.last_target_switch_time < self.target_switch_delay:
            return  # Δεν είναι ώρα για αλλαγή στόχου ακόμα
        
        alive_players = [player for player in self.players_group if player.alive]
        if alive_players:
            self.target = random.choice(alive_players)
        else:
            self.target = None
        self.last_target_switch_time = now
        

    def move_ai(self):

        if not self.target or not self.target.alive:
            return  # Δεν υπάρχει παίκτης ή ο παίκτης δεν είναι ζωντανός
        
       
        base_target = pygame.Vector2(self.target.rect.centerx, self.target.rect.centery - 500)
        time = pygame.time.get_ticks() * 0.005  # Ρυθμός ταλάντωσης
        bounce = math.sin(time) * 100  # Πλάτος ταλάντωσης
        target = pygame.Vector2(base_target.x + bounce, base_target.y)

        lerp_factor = 0.05
        self.pos = self.pos.lerp(target, lerp_factor)

        self.rect.center = (int(self.pos.x), int(self.pos.y))

    def shoot(self):
        if not self.target or not self.target.alive:
            return  # Δεν υπάρχει παίκτης ή ο παίκτης δεν είναι ζωντανός

        now = pygame.time.get_ticks()
        if now - self.last_shoot_time < self.shoot_delay:
            return  # Δεν είναι ώρα για πυροβολισμό ακόμα
        
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance == 0: distance = 1
        bullet_vx = dx / distance
        bullet_vy = dy / distance

        bullet = Bullet.from_shooter(
            shooter=self,
            width=8,
            height=12,
            speed=5.0,
            vx=bullet_vx,
            vy=bullet_vy,
            use_img=True,
            image_path= bullet_images,
        )

        self.bullets_group.add(bullet)
        self.last_shoot_time = now


    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.die() 
        print(f"BossEnemy took {damage} damage, HP left: {self.hp}")
    
    def die(self):
        self.alive = False
        self.kill()
        self.target.score += 100
        # Εδώ μπορεί να προστεθεί λογική για animation θανάτου ή αφαίρεση από το παιχνίδι

    def update(self, *args, **kwargs):
        if not self.alive:
            return
        self.target_player()
        self.move_ai()
        self.shoot()
        self.rect.center = (int(self.x), int(self.y))
        #super().update(*args, **kwargs)
        