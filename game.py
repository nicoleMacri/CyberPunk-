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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("CYBER RUNNER")

# Ρυθμίσεις γραμματοσειράς
FONT_LARGE = pygame.font.SysFont('Arial', 72) # Θα αλλαχθεί με καποία που ταιρίαζει πιο πολύ στο θέμα
FONT_MEDIUM = pygame.font.SysFont('Arial', 36)
FONT_SMALL = pygame.font.SysFont('Arial', 24)

# Ρυθμίσεις ρολογιού
clock = pygame.time.Clock() 

# Settings για τα αντικείμενα enemies
settings = [
    (random.randint(50, SCREEN_WIDTH - 90), # Τυχαία θέση x εντός οθόνης
     random.randint(50, SCREEN_HEIGHT - 200), # Τυχαία θέση y εντός οθόνης
     random.choice(enemies_colors), # Τυχαίο χρώμα από τη λίστα με τα χρώματα των εχθρών
     random.uniform(1.0, 5.0), # Τυχαία ταχύτητα μεταξύ 1.0 και 5.0
     random.choice(["left", "right", "up", "down"])) # Τυχαία κατεύθυνση κίνησης
    for _ in range(5) # Δημιουργία 5 εχθρών
]

# Δημιουργία λίστας με αντικείμενα Enemy
enemies = [Enemy(x, y, 40, 40, color, speed, direction) for x, y, color, speed, direction in settings]

# Δημιουργία αντικειμένου Player
player = Player( SCREEN_WIDTH, SCREEN_HEIGHT, 50, 50, SKY_BLUE, 5)

# Δημιουργία αντικειμένου PowerUp
power_up = PowerUp(300, 0, 30, 30, BLACK, 2)

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
        enemy.auto_move()  # Κίνηση του εχθρού προς τα δεξιά
        enemy.draw(screen)
    
    power_up.activate()  # Ενεργοποίηση του power-up
    power_up.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)