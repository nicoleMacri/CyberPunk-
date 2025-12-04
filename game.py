"""
Βασική δομή παιχνιδιού CYBER RUNNER
Περιλαμβάνει την αρχικοποίηση του παραθύρου, τη δημιουργία αντικειμένων παίκτη, εχθρών,
σφαιρών και power-ups, καθώς και την κύρια λούπα του παιχνιδιού για την επεξεργασία εισόδου,
την ενημέρωση της κατάστασης των αντικειμένων και τη σχεδίαση τους.

"""
import pygame
import random

# Εισαγωγή κλάσεων 
from player import Player
from enemy import Enemy
from powerups import PowerUp
from enemyWave import EnemyWave

# Αρχικοποίηση της βιβλιοθήκης Pygame
pygame.init()

# Ορισμός χρωμάτων
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RUSSIAN_VIOLET = (52, 27, 95)
HOLLYWOOD_CERISE = (236, 19, 164)
AUREOLIN = (245, 230, 18)
ELECTRIC_INDIGO = (99, 57, 235)
SKY_BLUE = (94, 217, 242)

# Ρυθμίσεις παραθύρου
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER RUNNER")
backgrpund_img = pygame.image.load("background.jpg").convert()

# Ρυθμίσεις ρολογιού
clock = pygame.time.Clock() 

# Ρυθμίσεις γραμματοσειράς (Δεν χρησιμοποιούνται ακόμα)
FONT_LARGE = pygame.font.SysFont('Arial', 72) # Θα αλλαχθεί με καποία που ταιρίαζει πιο πολύ στο θέμα
FONT_MEDIUM = pygame.font.SysFont('Arial', 36)
FONT_SMALL = pygame.font.SysFont('Arial', 24)

# Δημιουργία groups για τα sprites 
player_bullets_group = pygame.sprite.Group()
enemy_bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# Αρχικοποιήση αντικειμένου παίκτη
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, 40, 40 , SKY_BLUE, 5)

# Δημιουργία του wave manager
wave_manager = EnemyWave(SCREEN_WIDTH, SCREEN_HEIGHT, enemies_group, enemy_bullets_group, player_bullets_group, player)
wave_manager.new_enemy_wave() # Δημιουργία νέου κύματος εχθρών


# ------------------------------------
# --------- GAME MAIN LOOP -----------
# ------------------------------------
done = False
while not done:
    now = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Επεξεργασία εισόδου χρήστη
    player.import_handler(SCREEN_WIDTH, player_bullets_group)
    
    #----- UPDATES -----
    # Ενημέρωση σφαιρών
    player_bullets_group.update()
    enemy_bullets_group.update()

    enemies_group.update()
    
    # Ενημέρησω κύματος εχθρών
    wave_manager.update()

    
    
    #----- Collisions ----- 
    hits = pygame.sprite.groupcollide(enemies_group, player_bullets_group, False, True)
    for enemy, bullets in hits.items():
        enemy.take_damage(damage=len(bullets))

    # ----- ΣΧΕΔΙΑΣΗ -----
    # Σχεδίαση φόντου
    screen.blit(backgrpund_img, (0, 0))  
    # Σχεδίαση του αντικειμένου Player
    player.draw(screen)
    # Σχεδίαση όλων των εχθρών από το group
    enemies_group.draw(screen)
    # Σχεδίαση όλων των σφαιρών από το group
    player_bullets_group.draw(screen)
    enemy_bullets_group.draw(screen)
   
    # Ενημέρωση της οθόνης
    pygame.display.flip()
    clock.tick(60)

