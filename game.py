import pygame
import random

# Εισαγωγή κλάσεων Player και Enemy 
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

enemies_colors = [ELECTRIC_INDIGO, HOLLYWOOD_CERISE, AUREOLIN]

# Ρυθμίσεις παραθύρου
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER RUNNER")

# Ρυθμίσεις γραμματοσειράς
FONT_LARGE = pygame.font.SysFont('Arial', 72) # Θα αλλαχθεί με καποία που ταιρίαζει πιο πολύ στο θέμα
FONT_MEDIUM = pygame.font.SysFont('Arial', 36)
FONT_SMALL = pygame.font.SysFont('Arial', 24)

# Ρυθμίσεις ρολογιού
clock = pygame.time.Clock() 

# Δημιουργία groups
#all_sprites = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()

# Settings για τα αντικείμενα enemies
rows = random.randint(2,8) # Αριθμός σειρών εχθρών
cols = random.randint(2,5) # Αριθμός στηλών εχθρών
spacing_x = 80 # Κενό μεταξύ των εχθρών οριζόντια
spacing_y = 80 # Κενό μεταξύ των εχθρών κάθετα

grid_w = (cols - 0.5) * spacing_x 
grid_h = (rows - 1) * spacing_y

start_x = (SCREEN_WIDTH - grid_w) // 2
start_y = (SCREEN_HEIGHT - grid_h) // 4


# Διατηρηση 2d λίστας για τους εχθρούς για λογιή εμφάνισης 
enemies_grid = []
for row in range(rows):
    row_list = []
    for col in range(cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y
        color = random.choice(enemies_colors)
        speed = 1.0
        #speed = random.uniform(1.0, 5.0)
        direction = "down"
        #direction = random.choice(["left", "right", "up", "down"])
        enemy = Enemy(x, y, 40, 40, color, speed, direction, row, col)
        enemies_group.add(enemy)
        row_list.append(enemy)
    enemies_grid.append(row_list)

# Αρχικός δείκτης της τελευταίας σειράς
last_row = rows - 1


# Δημιουργία αντικειμένου Player
player = Player( SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, SKY_BLUE, 5)

# Δημιουργία αντικειμένου PowerUp
#power_up = PowerUp(300, 0, 30, 30, BLACK, 1)

# Κύρια λούπα παιχνιδιού
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    # Επεξεργασία εισόδου χρήστη
    player.import_handler(SCREEN_WIDTH, bullets_group)
    # Ενημέρωση εχθρών: περνάμε την τελευταία σειρά (last_row) ως postional arg (συμβατό με Group.update)
    enemies_group.update(last_row)
    # ΤΟDO: update και για τα power-ups, bullets κλπ
    # Ενημέρωση σφαίρων
    bullets_group.update()
    
    screen.fill(RUSSIAN_VIOLET)
    # Σχεδίαση του αντικειμένου Player
    player.draw(screen)
    # Σχεδίαση όλων των εχθρών από το group
    enemies_group.draw(screen)
    bullets_group.draw(screen)
    
   
    
    pygame.display.flip()
    clock.tick(60)

