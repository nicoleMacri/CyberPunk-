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

# Λίστα με χρώματα για τους εχθρούς ( Αργότερα θα αντικατασταθεί με τα sprites των εχθρών)
enemies_colors = [ELECTRIC_INDIGO, HOLLYWOOD_CERISE, AUREOLIN]

# Ρυθμίσεις παραθύρου
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER RUNNER")

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

# ------- Settings για το grid για τα αντικείμενα enemies ----------
""" 
Δημιουργία ενός πλέυγματος (grid) εχθρών με τυχαίο αριθμό σειρών και στηλών. Ουσιαστικά,
δημιουργούμε μια 2D διάταξη εχθρών που τοποθετούνται σε συγκεκριμένες αποστάσεις (spacing) μεταξύ τους.
, με οργανωμένη διάταξη στην οθόνη, ώστε να μπορούμε να τους διαχειριστούμε πιο εύκολα.
"""
# TODO: Να προστεθεί λογική για διαφορετικό μέγεθος grid αναλογα με το επιπεδο δυσκολίας
rows = random.randint(2,4) # 2 εως 4 σειρές
cols = random.randint(3,5) # 3 εως 6 στήλες
spacing_x = 80 # Απόσταση μεταξύ στηλών
spacing_y = 80 # Απόσταση μεταξύ σειρών

grid_w = (cols - 0.5) * spacing_x # Πλάτος του grid
grid_h = (rows - 1) * spacing_y # Ύψος του grid

start_x = (SCREEN_WIDTH - grid_w) // 2 # Κεντράρισμα οριζόντια στο κέντρο της οθόνης
start_y = (SCREEN_HEIGHT - grid_h) // 4 #Κεντράρισμα κάθετα στο άνω μέρος της οθόνης

row_switch_cooldown = 200 
last_row_switch_time = 0


# Δημιουργία του wave manager
wave_manager = EnemyWave(SCREEN_WIDTH, SCREEN_HEIGHT, enemies_group, enemy_bullets_group, player_bullets_group)
wave_manager.new_enemy_wave() # Δημιουργία νέου κύματος εχθρών

# Αρχικοποιήση αντικειμένου παίκτη
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, SKY_BLUE, 5)




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
    wave_manager.new_enemy_wave()

    #----- UPDATES -----
    
    # Ενημέρωση σφαιρών
    player_bullets_group.update()
    enemy_bullets_group.update()

    # Ενημέρησω κύματος εχθρών
    wave_manager.update()
    
    #----- Collisions ----- 
    #handle_collisions()
    hits = pygame.sprite.groupcollide(enemies_group, player_bullets_group, False, True)
    for enemy, bullets in hits.items():
        enemy.take_damage(damage=len(bullets))

    # πυροβολισμοί εψθρού
    #for enemy in list(enemies_group):
    #    if enemy.row == active_row and rows_status[active_row]['activated']:
    #        enemy.shoot(enemy_bullets_group)    



    
    
    
    # ----- ΣΧΕΔΙΑΣΗ -----
    # Σχεδίαση
    screen.fill(RUSSIAN_VIOLET)
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

