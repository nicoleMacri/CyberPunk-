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
bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# Settings για το grid για τα αντικείμενα enemies
""" 
Δημιουργία ενός πλέυγματος (grid) εχθρών με τυχαίο αριθμό σειρών και στηλών. Ουσιαστικά,
δημιουργούμε μια 2D διάταξη εχθρών που τοποθετούνται σε συγκεκριμένες αποστάσεις (spacing) μεταξύ τους.
, με οργανωμένη διάταξη στην οθόνη, ώστε να μπορούμε να τους διαχειριστούμε πιο εύκολα.
"""
rows = random.randint(2,4) # 2 εως 4 σειρές
cols = random.randint(3,6) # 3 εως 6 στήλες
spacing_x = 80 # Απόσταση μεταξύ στηλών
spacing_y = 80 # Απόσταση μεταξύ σειρών

grid_w = (cols - 0.5) * spacing_x # Πλάτος του grid
grid_h = (rows - 1) * spacing_y # Ύψος του grid

start_x = (SCREEN_WIDTH - grid_w) // 2 # Κεντράρισμα οριζόντια στο κέντρο της οθόνης
start_y = (SCREEN_HEIGHT - grid_h) // 4 #Κεντράρισμα κάθετα στο άνω μέρος της οθόνης


# Διατηρηση 2d λίστας για τους εχθρούς για λογιή εμφάνισης 
enemies_grid = []
"""
[ 
    [Enemy1, Enemy2, ...],  # Σειρά 0
    [Enemy1, Enemy2, ...],  # Σειρά 1
    ...
]
"""
for row in range(rows):
    row_list = []
    for col in range(cols):
        x = start_x + col * spacing_x # Οριζόντια μετατόπιση
        y = start_y + row * spacing_y # Κατακόρυφη μετατόπιση
        color = random.choice(enemies_colors) # Τυχαίο χρώμα από τη λίστα
        speed = random.uniform(1.0, 5.0) # Τυχαία ταχύτητα μεταξύ 1.0 και 5.0
        direction = "down"
        #direction = random.choice(["left", "right", "up", "down"])
        enemy = Enemy(x, y, 30, 30, color, speed, direction, row, col, enemies_group)
        row_list.append(enemy)
    enemies_grid.append(row_list)



# Αρχικός δείκτης της τελευταίας σειράς
active_row = rows - 1

# Δημιουργία αντικειμένου Player
player = Player( SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, SKY_BLUE, 5)

# ------------------------------------
# ------ Κύρια λούπα παιχνιδιού ------
# ------------------------------------
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Επεξεργασία εισόδου χρήστη
    player.import_handler(SCREEN_WIDTH, bullets_group)
    # Ενημέρωση εχθρών: περνάμε την τελευταία σειρά (active_row) ως postional arg (συμβατό με Group.update)
    enemies_group.update(active_row)
    # ΤΟDO: update και για τα power-ups, bullets κλπ
    for e in enemies_group:
        if e.row == active_row:
            e.shoot(bullets_group)
    # Ενημέρωση σφαίρων
    bullets_group.update()
 

    # Σχεδίαση
    screen.fill(RUSSIAN_VIOLET)
    # Σχεδίαση του αντικειμένου Player
    player.draw(screen)
    # Σχεδίαση όλων των εχθρών από το group
    enemies_group.draw(screen)
    # Σχεδίαση όλων των σφαιρών από το group
    bullets_group.draw(screen)
    
   
    # Ενημέρωση της οθόνης
    pygame.display.flip()
    clock.tick(60)

