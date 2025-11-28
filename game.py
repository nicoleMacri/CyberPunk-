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
from bullet import Bullet

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

# Ρυθμίσεις γραμματοσειράς (Δεν χρησιμοποιούνται ακόμα)
FONT_LARGE = pygame.font.SysFont('Arial', 72) # Θα αλλαχθεί με καποία που ταιρίαζει πιο πολύ στο θέμα
FONT_MEDIUM = pygame.font.SysFont('Arial', 36)
FONT_SMALL = pygame.font.SysFont('Arial', 24)

# Ρυθμίσεις ρολογιού
clock = pygame.time.Clock() 

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

# ----- Βοηθητικές μέθοδοι ------
def create_enemies_grid():
    """
    Δημιουργεί ένα grid εχθρών με τυχαία χαρακτηριστικά και τους προσθέτει στο enemies_group.
    Επιστρέφει μια 2D λίστα με τους εχθρούς.
    enemies_grid_local: [
        [Enemy00, Enemy01, ...],  # Σειρά 0
        [Enemy10, Enemy11, ...],  # Σειρά 1
        [...],                    # ...
    ]
    """
    enemies_grid_local = []
    for row in range(rows):
        row_list = []
        for col in range(cols):
            x = start_x + col * spacing_x # Οριζόντια μετατόπιση
            y = start_y + row * spacing_y # Κατακόρυφη μετατόπιση
            color = random.choice(enemies_colors) # Τυχαίο χρώμα από τη λίστα
            #speed = random.uniform(1.0, 5.0) # Τυχαία ταχύτητα μεταξύ 1.0 και 5.0
            #direction = "down"
            #direction = random.choice(["left", "right", "up", "down"])
            enemy = Enemy(x, y, 30, 30, color, speed = 2.0 , direction="down", row=row, col=col,
                            bullets_group=enemy_bullets_group,
                            shoot_delay=2000,
                            row_height=spacing_y,
                            hp=10)
            enemies_group.add(enemy) # Προσθήκη του εχθρού στο group
            row_list.append(enemy) # Προσθήκη του εχθρού στη σειρά
        enemies_grid_local.append(row_list) # Προσθήκη της σειράς στο grid
    return enemies_grid_local # Επιστροφή του grid εχθρών

# Επιστρόφει μια λίστα με την κατάσταση ενεργοποίησης των σειρών
def init_rows_status(rows):
    return [{'activated': False, 'start_time': None} for _ in range(rows)]

def activate_row(idx, row_status, enemies_grid, spacing_y):
    """
    rows_status: [
        {'activated': False, 'start_time': None},  # Σειρά 0
        {'activated': False, 'start_time': None},  # Σειρά 1
        ...
    ]
    """
    now = pygame.time.get_ticks()
    rows_status[idx]['activated'] = True
    rows_status[idx]['start_time'] = now
    for e in enemies_grid[idx]:
        e.activate(row_height=spacing_y)


def row_cleared(idx, enemies_grid, enemies_group):
    for e in enemies_grid[idx]:
        if e in enemies_group:
            return False
    return True


def respawn_grid():
    enemies_group.empty()
    enemy_bullets_group.empty()
    player_bullets_group.empty()
    new_grid = create_enemies_grid()
    new_rows_status = init_rows_status(rows)
    activate_row(0, new_rows_status, new_grid, spacing_y)
    return new_grid, new_rows_status, 0

def handle_collisions():
    hits = pygame.sprite.groupcollide(enemies_group, player_bullets_group, False, True)
    for enemy, bullets in hits.items():
        enemy.take_damage(damage=len(bullets))


# ----- Αρχικοποίηση αντικειμενών 

# Αρχικοποιήση αντικειμένου παίκτη
player = Player(SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, SKY_BLUE, 5)

# Δημιουργία του grid εχθρών
enemies_grid = create_enemies_grid()
rows_status = init_rows_status(rows)
active_row = 0
activate_row(active_row, rows_status, enemies_grid, spacing_y)




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
    
    # Ενημέρωση εχθρών: περνάμε την τελευταία σειρά (active_row) ως postional arg (συμβατό με Group.update)
    enemies_group.update(active_row=active_row)
    
    # Ενημέρωση σφαιρών
    player_bullets_group.update()
    enemy_bullets_group.update()

    # Collisions 
    handle_collisions()

    # πυροβολισμοί εψθρού
    for enemy in list(enemies_group):
        if enemy.row == active_row and rows_status[active_row]['activated']:
            enemy.shoot(enemy_bullets_group)    


    if row_cleared(active_row, enemies_grid, enemies_group):
        if active_row < rows - 1 and (now - last_row_switch_time ) >= row_switch_cooldown:
            active_row += 1
            last_row_switch_time = now
            activate_row(active_row, rows_status, enemies_grid, spacing_y)
        else:
            all_cleared = all(row_cleared(r, enemies_grid, enemies_group) for r in range(rows))
            if all_cleared:
                enemies_grid, rows_status, active_row = respawn_grid()
    
    
    

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

