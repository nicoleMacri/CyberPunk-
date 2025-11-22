import pygame
import random

# Εισαγωγή κλάσεων Player και Enemy 
from player import Player
from enemy import Enemy
from powerups import PowerUp

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


# Settings για τα αντικείμενα enemies
enemies = [] # Λίστα για αποθήκευση των εχθρών
rows = random.randint(2,8) # Αριθμός σειρών εχθρών
cols = random.randint(2,5) # Αριθμός στηλών εχθρών
spacing_x = 80 # Κενό μεταξύ των εχθρών οριζόντια

grid_w = (cols - 0.5) * spacing_x 
grid_h = (rows - 1) * spacing_x

start_x = (SCREEN_WIDTH - grid_w) // 2
start_y = (SCREEN_HEIGHT - grid_h) // 4



for row in range(rows):
    for col in range(cols):
        x = start_x + col * spacing_x
        y = start_y + row * spacing_x
        color = random.choice(enemies_colors)
        speed = 1.0
        #speed = random.uniform(1.0, 5.0)
        direction = "down"
        #direction = random.choice(["left", "right", "up", "down"])
        enemy = Enemy(x, y, 40, 40, color, speed, direction)
        enemies.append(enemy)

last_row = enemies[(rows - 1) * cols : rows * cols]

#num_enemies = random.randint(3, 7)  # Τυχαίος αριθμός εχθρών μεταξύ 3 και 7
#settings = [
#    (
#     40, 80,
#     random.choice(enemies_colors), # Τυχαίο χρώμα από τη λίστα με τα χρώματα των εχθρών
#     random.uniform(1.0, 5.0), # Τυχαία ταχύτητα μεταξύ 1.0 και 5.0
#     random.choice(["left", "right", "up", "down"])) # Τυχαία κατεύθυνση κίνησης
#    for _ in range(num_enemies) # Δημιουργία 5 εχθρών
#]
# Δημιουργία λίστας με αντικείμενα Enemy
#enemies = [Enemy(x, y, 40, 40, color, speed, direction) for x, y, color, speed, direction in settings]



# Δημιουργία αντικειμένου Player
player = Player( SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, SKY_BLUE, 5)

# Δημιουργία αντικειμένου PowerUp
power_up = PowerUp(300, 0, 30, 30, BLACK, 1)

# Κύρια λούπα παιχνιδιού
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    player.import_handler(SCREEN_WIDTH)
    screen.fill(RUSSIAN_VIOLET)
    player.draw(screen)
    
    for enemy in enemies:
        enemy.draw(screen)
    for enemy in last_row:  # Κίνηση μόνο για τους πρώτους εχθρούς
        enemy.auto_move()
    
    power_up.activate()  # Ενεργοποίηση του power-up
    power_up.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

